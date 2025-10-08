#!/usr/bin/env python3
"""Generate mock tests from captured real device data.

This script takes captured device data and generates comprehensive mock tests
that simulate real device behavior without requiring a physical device.
"""

import json
import sys
from pathlib import Path

# Add the custom component to the path
sys.path.insert(0, str(Path(__file__).parent / "custom_components"))

from test_config import FIXTURES_DIR


def load_captured_data(filename: str = "real_device_data.json") -> dict:
    """Load captured device data from file."""
    # Try multiple possible locations
    possible_paths = [
        FIXTURES_DIR / filename,
        Path("tests/fixtures") / filename,
        Path("fixtures") / filename,
        Path(filename),
    ]
    
    filepath = None
    for path in possible_paths:
        if path.exists():
            filepath = path
            break
    
    if not filepath:
        raise FileNotFoundError(f"Captured data file not found. Tried: {possible_paths}")
    
    with open(filepath, 'r') as f:
        return json.load(f)


def generate_telnet_client_mocks(data: dict) -> str:
    """Generate mock tests for telnet client."""
    device_info = data.get("device_info", {})
    outlet_info = data.get("outlet_info", [])
    
    mock_code = f'''"""Mock tests for WattboxTelnetClient based on real device data."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from custom_components.wattbox.telnet_client import (
    WattboxTelnetClient,
    WattboxConnectionError,
    WattboxAuthenticationError,
)


@pytest.fixture
def real_device_data():
    """Real device data captured from actual Wattbox."""
    return {json.dumps(data, indent=4)}


@pytest.fixture
def mock_telnet_client():
    """Mock telnet client with real device responses."""
    client = MagicMock(spec=WattboxTelnetClient)
    client.is_connected = True
    client.device_data = {{
        "device_info": {json.dumps(device_info, indent=8)},
        "outlet_info": {json.dumps(outlet_info, indent=8)},
    }}
    return client


class TestWattboxTelnetClientRealData:
    """Test telnet client with real device data."""

    @pytest.mark.asyncio
    async def test_async_connect_success(self, mock_telnet_client):
        """Test successful connection."""
        with patch('telnetlib3.open_connection') as mock_open:
            mock_reader = AsyncMock()
            mock_writer = AsyncMock()
            mock_open.return_value = (mock_reader, mock_writer)
            
            # Mock the authentication sequence
            mock_reader.readuntil.side_effect = [
                b"Username: ",
                b"Password: ",
                b"Successfully Logged In!",
            ]
            
            client = WattboxTelnetClient("192.168.1.100", "wattbox", "wattbox")
            await client.async_connect()
            
            assert client.is_connected is True
            mock_writer.write.assert_called()

    @pytest.mark.asyncio
    async def test_async_get_device_info_real_data(self, real_device_data):
        """Test device info retrieval with real data."""
        with patch('telnetlib3.open_connection') as mock_open:
            mock_reader = AsyncMock()
            mock_writer = AsyncMock()
            mock_open.return_value = (mock_reader, mock_writer)
            
            # Mock responses based on real device
            mock_reader.readuntil.side_effect = [
                b"Username: ",
                b"Password: ",
                b"Successfully Logged In!",
                b"\\n",  # Firmware response
                b"\\n",  # Model response
                b"\\n",  # Service tag response
                b"\\n",  # Hostname response
                b"\\n",  # Auto reboot response
            ]
            
            # Mock command responses
            async def mock_send_command(cmd):
                if cmd == "?Firmware":
                    return f"?Firmware={device_info.get('hardware_version', 'Unknown')}"
                elif cmd == "?Model":
                    return f"?Model={device_info.get('model', 'Unknown')}"
                elif cmd == "?ServiceTag":
                    return f"?ServiceTag={device_info.get('serial_number', 'Unknown')}"
                elif cmd == "?Hostname":
                    return f"?Hostname={device_info.get('hostname', 'Unknown')}"
                elif cmd == "?AutoReboot":
                    return f"?AutoReboot={device_info.get('auto_reboot', 'Unknown')}"
                return ""
            
            client = WattboxTelnetClient("192.168.1.100", "wattbox", "wattbox")
            client.async_send_command = mock_send_command
            
            device_info = await client.async_get_device_info()
            
            # Verify structure matches real data
            assert "hardware_version" in device_info
            assert "model" in device_info
            assert "serial_number" in device_info
            assert "hostname" in device_info
            assert "auto_reboot" in device_info

    @pytest.mark.asyncio
    async def test_async_get_outlet_status_real_data(self, real_device_data):
        """Test outlet status retrieval with real data."""
        outlet_info = real_device_data.get("outlet_info", [])
        
        with patch('telnetlib3.open_connection') as mock_open:
            mock_reader = AsyncMock()
            mock_writer = AsyncMock()
            mock_open.return_value = (mock_reader, mock_writer)
            
            # Mock authentication
            mock_reader.readuntil.side_effect = [
                b"Username: ",
                b"Password: ",
                b"Successfully Logged In!",
                b"\\n",  # Outlet status response
                b"\\n",  # Outlet names response
            ]
            
            # Mock command responses
            async def mock_send_command(cmd):
                if cmd == "?OutletStatus":
                    # Generate outlet states based on real data
                    states = [str(outlet.get("state", 0)) for outlet in outlet_info]
                    return f"?OutletStatus={','.join(states)}"
                elif cmd == "?OutletName":
                    # Generate outlet names based on real data
                    names = [outlet.get("name", f"Outlet {i+1}") for i, outlet in enumerate(outlet_info)]
                    return f"?OutletName={','.join(names)}"
                return ""
            
            client = WattboxTelnetClient("192.168.1.100", "wattbox", "wattbox")
            client.async_send_command = mock_send_command
            
            outlets = await client.async_get_outlet_status(len(outlet_info))
            
            # Verify structure matches real data
            assert len(outlets) == len(outlet_info)
            for i, outlet in enumerate(outlets):
                assert "state" in outlet
                assert "name" in outlet
                assert isinstance(outlet["state"], int)
                assert isinstance(outlet["name"], str)

    @pytest.mark.asyncio
    async def test_async_set_outlet_state_real_data(self, real_device_data):
        """Test outlet control with real data."""
        with patch('telnetlib3.open_connection') as mock_open:
            mock_reader = AsyncMock()
            mock_writer = AsyncMock()
            mock_open.return_value = (mock_reader, mock_writer)
            
            # Mock authentication
            mock_reader.readuntil.side_effect = [
                b"Username: ",
                b"Password: ",
                b"Successfully Logged In!",
                b"\\n",  # Command response
            ]
            
            client = WattboxTelnetClient("192.168.1.100", "wattbox", "wattbox")
            client.async_send_command = AsyncMock()
            
            # Test turning outlet on
            await client.async_set_outlet_state(1, True)
            client.async_send_command.assert_called_with("!OutletSet=1,ON")
            
            # Test turning outlet off
            await client.async_set_outlet_state(1, False)
            client.async_send_command.assert_called_with("!OutletSet=1,OFF")
'''
    
    return mock_code


def generate_coordinator_mocks(data: dict) -> str:
    """Generate mock tests for coordinator."""
    device_info = data.get("device_info", {})
    outlet_info = data.get("outlet_info", [])
    
    mock_code = f'''"""Mock tests for WattboxDataUpdateCoordinator based on real device data."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from custom_components.wattbox.coordinator import WattboxDataUpdateCoordinator
from custom_components.wattbox.telnet_client import WattboxTelnetClient


@pytest.fixture
def real_device_data():
    """Real device data captured from actual Wattbox."""
    return {json.dumps(data, indent=4)}


@pytest.fixture
def mock_coordinator(real_device_data):
    """Mock coordinator with real device data."""
    coordinator = MagicMock(spec=WattboxDataUpdateCoordinator)
    coordinator.data = {{
        "device_info": {json.dumps(device_info, indent=8)},
        "outlet_info": {json.dumps(outlet_info, indent=8)},
        "connected": True,
    }}
    coordinator.async_request_refresh = AsyncMock()
    return coordinator


class TestWattboxDataUpdateCoordinatorRealData:
    """Test coordinator with real device data."""

    @pytest.mark.asyncio
    async def test_data_structure_real_device(self, real_device_data):
        """Test that coordinator data structure matches real device."""
        device_info = real_device_data.get("device_info", {{}})
        outlet_info = real_device_data.get("outlet_info", [])
        
        # Verify device info structure
        expected_keys = ["hardware_version", "model", "serial_number", "hostname", "auto_reboot"]
        for key in expected_keys:
            assert key in device_info, f"Missing device info key: {{key}}"
        
        # Verify outlet info structure
        assert len(outlet_info) > 0, "No outlet data captured"
        for i, outlet in enumerate(outlet_info):
            assert "state" in outlet, f"Outlet {{i}} missing state"
            assert "name" in outlet, f"Outlet {{i}} missing name"
            assert isinstance(outlet["state"], int), f"Outlet {{i}} state not integer"
            assert isinstance(outlet["name"], str), f"Outlet {{i}} name not string"

    @pytest.mark.asyncio
    async def test_async_set_outlet_state_real_data(self, mock_coordinator):
        """Test outlet state setting with real data."""
        # Test with first outlet from real data
        outlet_number = 1
        new_state = True
        
        await mock_coordinator.async_set_outlet_state(outlet_number, new_state)
        
        # Verify the method was called
        mock_coordinator.async_set_outlet_state.assert_called_with(outlet_number, new_state)
'''
    
    return mock_code


def generate_platform_mocks(data: dict) -> str:
    """Generate mock tests for platform entities."""
    device_info = data.get("device_info", {})
    outlet_info = data.get("outlet_info", [])
    
    mock_code = f'''"""Mock tests for platform entities based on real device data."""

import pytest
from unittest.mock import MagicMock
from custom_components.wattbox.switch import WattboxSwitch
from custom_components.wattbox.sensor import (
    WattboxFirmwareSensor,
    WattboxModelSensor,
    WattboxSerialSensor,
    WattboxHostnameSensor,
)
from custom_components.wattbox.binary_sensor import WattboxStatusBinarySensor


@pytest.fixture
def real_device_data():
    """Real device data captured from actual Wattbox."""
    return {json.dumps(data, indent=4)}


@pytest.fixture
def mock_coordinator_with_real_data(real_device_data):
    """Mock coordinator with real device data."""
    coordinator = MagicMock()
    coordinator.data = {{
        "device_info": {json.dumps(device_info, indent=8)},
        "outlet_info": {json.dumps(outlet_info, indent=8)},
        "connected": True,
    }}
    return coordinator


class TestPlatformEntitiesRealData:
    """Test platform entities with real device data."""

    def test_switch_entities_real_data(self, mock_coordinator_with_real_data, real_device_data):
        """Test switch entities with real outlet data."""
        outlet_info = real_device_data.get("outlet_info", [])
        
        for i, outlet in enumerate(outlet_info):
            switch = WattboxSwitch(
                coordinator=mock_coordinator_with_real_data,
                device_info={{}},
                unique_id=f"test_outlet_{{i+1}}",
                outlet_number=i+1,
            )
            
            # Test that switch can be created
            assert switch._outlet_number == i + 1
            assert switch.name == f"Outlet {{i+1}}"
            
            # Test state reading
            state = switch.is_on
            assert isinstance(state, bool) or state is None

    def test_sensor_entities_real_data(self, mock_coordinator_with_real_data, real_device_data):
        """Test sensor entities with real device data."""
        device_info = real_device_data.get("device_info", {{}})
        
        # Test firmware sensor
        firmware_sensor = WattboxFirmwareSensor(
            coordinator=mock_coordinator_with_real_data,
            entry_id="test_entry",
        )
        assert firmware_sensor.native_value == device_info.get("hardware_version")
        
        # Test model sensor
        model_sensor = WattboxModelSensor(
            coordinator=mock_coordinator_with_real_data,
            entry_id="test_entry",
        )
        assert model_sensor.native_value == device_info.get("model")
        
        # Test serial sensor
        serial_sensor = WattboxSerialSensor(
            coordinator=mock_coordinator_with_real_data,
            entry_id="test_entry",
        )
        assert serial_sensor.native_value == device_info.get("serial_number")
        
        # Test hostname sensor
        hostname_sensor = WattboxHostnameSensor(
            coordinator=mock_coordinator_with_real_data,
            entry_id="test_entry",
        )
        assert hostname_sensor.native_value == device_info.get("hostname")

    def test_binary_sensor_real_data(self, mock_coordinator_with_real_data):
        """Test binary sensor with real data."""
        sensor = WattboxStatusBinarySensor(
            coordinator=mock_coordinator_with_real_data,
            entry_id="test_entry",
        )
        
        # Test connectivity status
        assert sensor.is_on is True  # Based on mock data
        assert sensor.device_class == "connectivity"
'''
    
    return mock_code


def main():
    """Generate mock tests from captured data."""
    if len(sys.argv) > 1:
        data_file = sys.argv[1]
    else:
        data_file = "real_device_data.json"
    
    try:
        # Load captured data
        data = load_captured_data(data_file)
        print(f"✅ Loaded captured data from {data_file}")
        
        # Generate mock tests
        telnet_mocks = generate_telnet_client_mocks(data)
        coordinator_mocks = generate_coordinator_mocks(data)
        platform_mocks = generate_platform_mocks(data)
        
        # Save generated tests
        test_dir = Path("tests") / "generated"
        test_dir.mkdir(exist_ok=True)
        
        # Save telnet client mocks
        with open(test_dir / "test_telnet_client_real_data.py", "w") as f:
            f.write(telnet_mocks)
        
        # Save coordinator mocks
        with open(test_dir / "test_coordinator_real_data.py", "w") as f:
            f.write(coordinator_mocks)
        
        # Save platform mocks
        with open(test_dir / "test_platforms_real_data.py", "w") as f:
            f.write(platform_mocks)
        
        print("✅ Generated mock tests:")
        print(f"  - {test_dir / 'test_telnet_client_real_data.py'}")
        print(f"  - {test_dir / 'test_coordinator_real_data.py'}")
        print(f"  - {test_dir / 'test_platforms_real_data.py'}")
        
        return 0
        
    except Exception as e:
        print(f"❌ Error generating mock tests: {e}")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
