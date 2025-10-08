#!/usr/bin/env python3
"""Test script to connect to real Wattbox device and capture interactions.

This script will:
1. Connect to your Wattbox device
2. Capture all telnet commands and responses
3. Save the data for building mock tests
4. Test all functionality with real device

Usage:
    # Set environment variables:
    export WATTBOX_TEST_HOST=192.168.1.100
    export WATTBOX_TEST_USERNAME=wattbox
    export WATTBOX_TEST_PASSWORD=your_password
    python test_real_device.py
    
    # Or use command line arguments:
    python test_real_device.py --host 192.168.1.100 --username wattbox --password your_password
"""

import argparse
import asyncio
import json
import logging
import sys
from datetime import datetime
from pathlib import Path

# Add the custom component to the path
sys.path.insert(0, str(Path(__file__).parent / "custom_components"))

from wattbox.telnet_client import WattboxTelnetClient
from test_config import WATTBOX_TEST_CONFIG, TEST_SETTINGS, FIXTURES_DIR

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
_LOGGER = logging.getLogger(__name__)


class WattboxTestCapture:
    """Capture real device interactions for testing."""
    
    def __init__(self, host: str, username: str, password: str):
        """Initialize the test capture."""
        self.host = host
        self.username = username
        self.password = password
        self.client = WattboxTelnetClient(host, username, password)
        self.captured_data = {
            "timestamp": datetime.now().isoformat(),
            "device_info": {},
            "outlet_info": [],
            "commands_responses": [],
            "test_results": {}
        }
    
    async def capture_device_interaction(self) -> dict:
        """Capture all device interactions."""
        _LOGGER.info(f"Starting device interaction capture for {self.host}")
        
        try:
            # Test connection
            _LOGGER.info("Testing connection...")
            await self.client.async_connect()
            self.captured_data["test_results"]["connection"] = "SUCCESS"
            _LOGGER.info("✅ Connection successful")
            
            # Capture device info
            _LOGGER.info("Capturing device information...")
            device_info = await self.client.async_get_device_info()
            self.captured_data["device_info"] = device_info
            _LOGGER.info(f"✅ Device info captured: {device_info}")
            
            # Capture outlet status
            _LOGGER.info("Capturing outlet status...")
            outlet_info = await self.client.async_get_outlet_status(18)
            self.captured_data["outlet_info"] = outlet_info
            _LOGGER.info(f"✅ Outlet info captured: {len(outlet_info)} outlets")
            
            # Test outlet control (if safe to do so)
            _LOGGER.info("Testing outlet control...")
            await self._test_outlet_control()
            
            # Test disconnection
            _LOGGER.info("Testing disconnection...")
            await self.client.async_disconnect()
            self.captured_data["test_results"]["disconnection"] = "SUCCESS"
            _LOGGER.info("✅ Disconnection successful")
            
        except Exception as e:
            _LOGGER.error(f"❌ Error during capture: {e}")
            self.captured_data["test_results"]["error"] = str(e)
            raise
        
        return self.captured_data
    
    async def _test_outlet_control(self) -> None:
        """Test outlet control functionality (safely)."""
        try:
            # Test getting current state of outlet 1
            outlet_info = self.client.device_data.get("outlet_info", [])
            if outlet_info:
                outlet_1_state = outlet_info[0].get("state", 0)
                _LOGGER.info(f"Outlet 1 current state: {outlet_1_state}")
                
                # Test setting outlet 1 to same state (no change)
                await self.client.async_set_outlet_state(1, bool(outlet_1_state))
                _LOGGER.info("✅ Outlet control test completed (no state change)")
                self.captured_data["test_results"]["outlet_control"] = "SUCCESS"
            else:
                _LOGGER.warning("No outlet info available for testing")
                self.captured_data["test_results"]["outlet_control"] = "SKIPPED"
                
        except Exception as e:
            _LOGGER.error(f"❌ Outlet control test failed: {e}")
            self.captured_data["test_results"]["outlet_control"] = f"FAILED: {e}"
    
    def save_captured_data(self, filename: str = None) -> str:
        """Save captured data to file."""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"wattbox_capture_{timestamp}.json"
        
        filepath = Path("tests") / "fixtures" / filename
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'w') as f:
            json.dump(self.captured_data, f, indent=2)
        
        _LOGGER.info(f"✅ Captured data saved to {filepath}")
        return str(filepath)


async def main():
    """Main test function."""
    parser = argparse.ArgumentParser(description="Test Wattbox device and capture interactions")
    parser.add_argument("--host", help="Wattbox device IP address (overrides config)")
    parser.add_argument("--username", help="Username (overrides config)")
    parser.add_argument("--password", help="Password (overrides config)")
    parser.add_argument("--output", help="Output filename for captured data")
    parser.add_argument("--config", help="Path to config file")
    
    args = parser.parse_args()
    
    # Load configuration
    config = WATTBOX_TEST_CONFIG.copy()
    test_settings = TEST_SETTINGS.copy()
    
    # Override with command line arguments
    if args.host:
        config["host"] = args.host
    if args.username:
        config["username"] = args.username
    if args.password:
        config["password"] = args.password
    
    _LOGGER.info(f"Starting Wattbox device test with {config['host']}")
    
    try:
        # Create test capture instance
        capture = WattboxTestCapture(config["host"], config["username"], config["password"])
        
        # Capture device interactions
        captured_data = await capture.capture_device_interaction()
        
        # Save captured data
        FIXTURES_DIR.mkdir(parents=True, exist_ok=True)
        output_file = capture.save_captured_data(args.output)
        
        # Print summary
        print("\n" + "="*60)
        print("WATTBOX DEVICE TEST SUMMARY")
        print("="*60)
        print(f"Host: {config['host']}")
        print(f"Device Info: {captured_data['device_info']}")
        print(f"Outlets: {len(captured_data['outlet_info'])}")
        print(f"Test Results: {captured_data['test_results']}")
        print(f"Data saved to: {output_file}")
        print("="*60)
        
        return 0
        
    except Exception as e:
        _LOGGER.error(f"Test failed: {e}")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
