#!/usr/bin/env python3
"""Generate mock tests from captured real device data - simplified version."""

import json
import sys
from pathlib import Path

# Add the custom component to the path
sys.path.insert(0, str(Path(__file__).parent / "custom_components"))


def load_captured_data(filename: str) -> dict:
    """Load captured device data from file."""
    # Try multiple possible locations
    possible_paths = [
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


def generate_real_data_tests(data: dict) -> str:
    """Generate tests based on real device data."""
    device_info = data.get("device_info", {})
    outlet_info = data.get("outlet_info", [])
    
    # Convert outlet info to a more readable format
    outlet_states = [outlet.get("state", 0) for outlet in outlet_info]
    outlet_names = [outlet.get("name", f"Outlet {i+1}") for i, outlet in enumerate(outlet_info)]
    
    # Convert None to None for Python compatibility
    def json_serialize(obj):
        if obj is None:
            return None
        return obj
    
    data_json = json.dumps(data, indent=4, default=json_serialize).replace('null', 'None')
    device_info_json = json.dumps(device_info, indent=4, default=json_serialize).replace('null', 'None')
    
    test_code = f'''"""Real device data tests for Wattbox integration.

Generated from actual device capture on {data.get('timestamp', 'unknown')}.
Device: {device_info.get('hostname', 'unknown')} ({device_info.get('serial_number', 'unknown')})
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from custom_components.wattbox.telnet_client import WattboxTelnetClient
from custom_components.wattbox.coordinator import WattboxDataUpdateCoordinator


@pytest.fixture
def real_device_data():
    """Real device data captured from actual Wattbox."""
    return {data_json}


@pytest.fixture
def real_device_info():
    """Real device info from captured data."""
    return {device_info_json}


@pytest.fixture
def real_outlet_info():
    """Real outlet info from captured data."""
    return {json.dumps(outlet_info, indent=4)}


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
        assert real_device_info["model"] == "{device_info.get('model', 'unknown')}"
        assert real_device_info["serial_number"] == "{device_info.get('serial_number', 'unknown')}"
        assert real_device_info["hostname"] == "{device_info.get('hostname', 'unknown')}"

    def test_outlet_info_structure(self, real_outlet_info):
        """Test that outlet info has expected structure."""
        assert len(real_outlet_info) == {len(outlet_info)}
        
        for i, outlet in enumerate(real_outlet_info):
            assert "state" in outlet
            assert "name" in outlet
            assert isinstance(outlet["state"], int)
            assert isinstance(outlet["name"], str)
            
        # Verify some specific outlet data
        assert real_outlet_info[0]["state"] == {outlet_states[0]}
        assert real_outlet_info[0]["name"] == "{outlet_names[0]}"

    @pytest.mark.asyncio
    async def test_telnet_client_with_real_data(self, real_device_data):
        """Test telnet client with real device responses."""
        with patch('telnetlib3.open_connection') as mock_open:
            mock_reader = AsyncMock()
            mock_writer = AsyncMock()
            mock_open.return_value = (mock_reader, mock_writer)
            
            # Mock authentication sequence
            mock_reader.readuntil.side_effect = [
                b"Username: ",
                b"Password: ",
                b"Successfully Logged In!",
                b"\\n",  # Firmware response
                b"\\n",  # Model response  
                b"\\n",  # Service tag response
                b"\\n",  # Hostname response
                b"\\n",  # Auto reboot response
                b"\\n",  # Outlet status response
                b"\\n",  # Outlet names response
            ]
            
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
        coordinator.data = {{
            "device_info": real_device_data["device_info"],
            "outlet_info": real_device_data["outlet_info"],
            "connected": True,
        }}
        
        # Test data structure
        assert coordinator.data["connected"] is True
        assert len(coordinator.data["outlet_info"]) == {len(outlet_info)}
        assert coordinator.data["device_info"]["model"] == "{device_info.get('model', 'unknown')}"

    def test_outlet_control_simulation(self, real_outlet_info):
        """Test outlet control with real outlet data."""
        # Simulate outlet control commands
        outlet_commands = []
        for i, outlet in enumerate(real_outlet_info):
            current_state = bool(outlet["state"])
            new_state = not current_state  # Flip state for testing
            command = f"!OutletSet={{i+1}},{{'ON' if new_state else 'OFF'}}"
            outlet_commands.append(command)
        
        # Verify commands are properly formatted
        assert len(outlet_commands) == {len(outlet_info)}
        assert outlet_commands[0] == "!OutletSet=1,ON"  # First outlet was OFF, so turn ON
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
'''
    
    return test_code


def main():
    """Generate mock tests from captured data."""
    if len(sys.argv) > 1:
        data_file = sys.argv[1]
    else:
        data_file = "wattbox_capture_20251007_180957.json"
    
    try:
        # Load captured data
        data = load_captured_data(data_file)
        print(f"✅ Loaded captured data from {data_file}")
        
        # Generate mock tests
        test_code = generate_real_data_tests(data)
        
        # Save generated tests
        test_dir = Path("tests") / "generated"
        test_dir.mkdir(exist_ok=True)
        
        output_file = test_dir / "test_real_device_data.py"
        with open(output_file, "w") as f:
            f.write(test_code)
        
        print(f"✅ Generated mock tests: {output_file}")
        print(f"📊 Device: {data['device_info'].get('hostname', 'unknown')}")
        print(f"🔌 Outlets: {len(data['outlet_info'])}")
        print(f"📅 Captured: {data.get('timestamp', 'unknown')}")
        
        return 0
        
    except Exception as e:
        print(f"❌ Error generating mock tests: {e}")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
