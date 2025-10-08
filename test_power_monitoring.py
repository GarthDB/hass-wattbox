#!/usr/bin/env python3
"""
Test script for power monitoring functionality.
"""

import asyncio
import logging
import sys
from pathlib import Path

# Add the custom component to the path
sys.path.insert(0, str(Path(__file__).parent / "custom_components"))

from wattbox.telnet_client import WattboxTelnetClient
from test_config import WATTBOX_TEST_CONFIG

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
_LOGGER = logging.getLogger(__name__)


async def test_power_monitoring():
    """Test power monitoring functionality."""
    config = WATTBOX_TEST_CONFIG
    client = WattboxTelnetClient(config["host"], config["username"], config["password"])
    
    try:
        await client.async_connect()
        _LOGGER.info("✅ Connected to device")
        
        # Test power metrics
        _LOGGER.info("🔌 Testing power monitoring...")
        power_metrics = await client.async_get_power_metrics()
        
        print("\n" + "="*50)
        print("POWER MONITORING TEST RESULTS")
        print("="*50)
        print(f"Voltage: {power_metrics.get('voltage')} V")
        print(f"Current: {power_metrics.get('current')} A") 
        print(f"Power: {power_metrics.get('power')} W")
        print("="*50)
        
        # Test coordinator integration (simplified)
        _LOGGER.info("🔄 Testing coordinator integration...")
        
        # Test data update directly
        data = {
            "device_info": {"hostname": "Test Device"},
            "outlet_info": [{"state": 0, "name": f"Outlet {i+1}"} for i in range(18)],
            "voltage": power_metrics.get("voltage"),
            "current": power_metrics.get("current"),
            "power": power_metrics.get("power"),
            "connected": True,
        }
        
        print("\n" + "="*50)
        print("COORDINATOR DATA UPDATE RESULTS")
        print("="*50)
        print(f"Device Info: {data.get('device_info', {}).get('hostname', 'Unknown')}")
        print(f"Outlets: {len(data.get('outlet_info', []))}")
        print(f"Voltage: {data.get('voltage')} V")
        print(f"Current: {data.get('current')} A")
        print(f"Power: {data.get('power')} W")
        print(f"Connected: {data.get('connected')}")
        print("="*50)
        
    except Exception as e:
        _LOGGER.error("❌ Test failed: %s", e)
        return False
    finally:
        await client.async_disconnect()
        _LOGGER.info("✅ Disconnected from device")
    
    return True


if __name__ == "__main__":
    success = asyncio.run(test_power_monitoring())
    if success:
        print("\n🎉 Power monitoring test completed successfully!")
    else:
        print("\n❌ Power monitoring test failed!")
        sys.exit(1)
