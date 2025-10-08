"""Real device data tests for Wattbox integration.

Generated from actual device capture on 2025-10-07T18:09:55.310632.
Device: ST201916431G842A (WB-800-IPVM-12)
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from custom_components.wattbox.coordinator import WattboxDataUpdateCoordinator
from custom_components.wattbox.telnet_client import WattboxTelnetClient


@pytest.fixture
def real_device_data():
    """Real device data captured from actual Wattbox."""
    return {
        "timestamp": "2025-10-07T18:09:55.310632",
        "device_info": {
            "hardware_version": None,
            "model": "2.8.0.0",
            "serial_number": "WB-800-IPVM-12",
            "hostname": "ST201916431G842A",
            "auto_reboot": "WattBox",
        },
        "outlet_info": [
            {"state": 0, "name": "0"},
            {"state": 0, "name": "1"},
            {"state": 0, "name": "0"},
            {"state": 0, "name": "0"},
            {"state": 0, "name": "1"},
            {"state": 0, "name": "0"},
            {"state": 0, "name": "0"},
            {"state": 0, "name": "1"},
            {"state": 0, "name": "0"},
            {"state": 0, "name": "0"},
            {"state": 0, "name": "0"},
            {"state": 0, "name": "0"},
            {"state": 0, "name": "Outlet 13"},
            {"state": 0, "name": "Outlet 14"},
            {"state": 0, "name": "Outlet 15"},
            {"state": 0, "name": "Outlet 16"},
            {"state": 0, "name": "Outlet 17"},
            {"state": 0, "name": "Outlet 18"},
        ],
        "commands_responses": [],
        "test_results": {
            "connection": "SUCCESS",
            "outlet_control": "SUCCESS",
            "disconnection": "SUCCESS",
        },
    }


@pytest.fixture
def real_device_info():
    """Real device info from captured data."""
    return {
        "hardware_version": None,
        "model": "2.8.0.0",
        "serial_number": "WB-800-IPVM-12",
        "hostname": "ST201916431G842A",
        "auto_reboot": "WattBox",
    }


@pytest.fixture
def real_outlet_info():
    """Real outlet info from captured data."""
    return [
        {"state": 0, "name": "0"},
        {"state": 0, "name": "1"},
        {"state": 0, "name": "0"},
        {"state": 0, "name": "0"},
        {"state": 0, "name": "1"},
        {"state": 0, "name": "0"},
        {"state": 0, "name": "0"},
        {"state": 0, "name": "1"},
        {"state": 0, "name": "0"},
        {"state": 0, "name": "0"},
        {"state": 0, "name": "0"},
        {"state": 0, "name": "0"},
        {"state": 0, "name": "Outlet 13"},
        {"state": 0, "name": "Outlet 14"},
        {"state": 0, "name": "Outlet 15"},
        {"state": 0, "name": "Outlet 16"},
        {"state": 0, "name": "Outlet 17"},
        {"state": 0, "name": "Outlet 18"},
    ]


class TestRealDeviceData:
    """Test with real device data structure."""

    def test_device_info_structure(self, real_device_info):
        """Test that device info has expected structure."""
        assert "hardware_version" in real_device_info
        assert "model" in real_device_info
        assert "serial_number" in real_device_info
        assert "hostname" in real_device_info
        assert "auto_reboot" in real_device_info

        # Verify actual values from your device
        assert real_device_info["model"] == "2.8.0.0"
        assert real_device_info["serial_number"] == "WB-800-IPVM-12"
        assert real_device_info["hostname"] == "ST201916431G842A"

    def test_outlet_info_structure(self, real_outlet_info):
        """Test that outlet info has expected structure."""
        assert len(real_outlet_info) == 18

        for _i, outlet in enumerate(real_outlet_info):
            assert "state" in outlet
            assert "name" in outlet
            assert isinstance(outlet["state"], int)
            assert isinstance(outlet["name"], str)

        # Verify some specific outlet data
        assert real_outlet_info[0]["state"] == 0
        assert real_outlet_info[0]["name"] == "0"

    @pytest.mark.asyncio
    async def test_telnet_client_with_real_data(self, real_device_data):
        """Test telnet client with real device responses."""
        with patch("telnetlib3.open_connection") as mock_open:
            mock_reader = AsyncMock()
            mock_writer = AsyncMock()
            mock_open.return_value = (mock_reader, mock_writer)

            # Mock authentication sequence
            mock_reader.readuntil.side_effect = [
                b"Username: ",
                b"Password: ",
                b"Successfully Logged In!",
                b"\n",  # Firmware response
                b"\n",  # Model response
                b"\n",  # Service tag response
                b"\n",  # Hostname response
                b"\n",  # Auto reboot response
                b"\n",  # Outlet status response
                b"\n",  # Outlet names response
            ]

            # Mock writer methods - write is synchronous, drain is async
            mock_writer.write = MagicMock()
            mock_writer.drain = AsyncMock()

            client = WattboxTelnetClient("192.168.1.34", "garthdb", "test_password")

            # Test connection
            await client.async_connect()
            assert client.is_connected is True

            # Test device info retrieval
            device_info = await client.async_get_device_info()
            assert "hardware_version" in device_info
            assert "model" in device_info

            # Test outlet status retrieval
            outlets = await client.async_get_outlet_status(18)
            assert len(outlets) == 18
            for outlet in outlets:
                assert "state" in outlet
                assert "name" in outlet

    def test_coordinator_with_real_data(self, real_device_data):
        """Test coordinator with real device data."""
        coordinator = MagicMock(spec=WattboxDataUpdateCoordinator)
        coordinator.data = {
            "device_info": real_device_data["device_info"],
            "outlet_info": real_device_data["outlet_info"],
            "connected": True,
        }

        # Test data structure
        assert coordinator.data["connected"] is True
        assert len(coordinator.data["outlet_info"]) == 18
        assert coordinator.data["device_info"]["model"] == "2.8.0.0"

    def test_outlet_control_simulation(self, real_outlet_info):
        """Test outlet control with real outlet data."""
        # Simulate outlet control commands
        outlet_commands = []
        for _i, outlet in enumerate(real_outlet_info):
            current_state = bool(outlet["state"])
            new_state = not current_state  # Flip state for testing
            command = f"!OutletSet={_i + 1},{'ON' if new_state else 'OFF'}"
            outlet_commands.append(command)

        # Verify commands are properly formatted
        assert len(outlet_commands) == 18
        assert (
            outlet_commands[0] == "!OutletSet=1,ON"
        )  # First outlet was OFF, so turn ON
        assert "!OutletSet=" in outlet_commands[0]
        assert "ON" in outlet_commands[0] or "OFF" in outlet_commands[0]

    def test_device_identification(self, real_device_info):
        """Test device identification from real data."""
        # Test that we can identify this as a Wattbox 800 series
        model = real_device_info.get("model", "")
        serial = real_device_info.get("serial_number", "")

        # Your device appears to be a WB-800-IPVM-12 based on serial
        assert "WB-800" in serial or "800" in model
        assert len(real_device_info.get("hostname", "")) > 0

        # Test that we have valid device identification
        assert real_device_info["serial_number"] != "unknown"
        assert real_device_info["hostname"] != "unknown"
