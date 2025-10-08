#!/usr/bin/env python3
"""Quick script to test with your actual Wattbox device."""

import asyncio
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add the custom component to the path
sys.path.insert(0, str(Path(__file__).parent / "custom_components"))

from wattbox.telnet_client import WattboxTelnetClient


async def test_device():
    """Test connection to your actual Wattbox device."""
    print("🔌 Testing connection to Wattbox device...")
    
    # Load device config from environment variables
    import os
    client = WattboxTelnetClient(
        host=os.getenv("WATTBOX_TEST_HOST", "192.168.1.100"),
        username=os.getenv("WATTBOX_TEST_USERNAME", "wattbox"), 
        password=os.getenv("WATTBOX_TEST_PASSWORD", "your_password_here")
    )
    
    try:
        # Test connection
        print("📡 Connecting...")
        await client.async_connect()
        print("✅ Connected successfully!")
        
        # Get device info
        print("📊 Getting device information...")
        device_info = await client.async_get_device_info()
        print(f"Device Info: {device_info}")
        
        # Get outlet status
        print("🔌 Getting outlet status...")
        outlet_info = await client.async_get_outlet_status(18)
        print(f"Found {len(outlet_info)} outlets:")
        for i, outlet in enumerate(outlet_info[:5]):  # Show first 5
            print(f"  Outlet {i+1}: {outlet['name']} - {'ON' if outlet['state'] else 'OFF'}")
        if len(outlet_info) > 5:
            print(f"  ... and {len(outlet_info) - 5} more outlets")
        
        # Test outlet control (safe - just set to current state)
        if outlet_info:
            current_state = bool(outlet_info[0]['state'])
            print(f"🔧 Testing outlet control (outlet 1, current state: {current_state})...")
            await client.async_set_outlet_state(1, current_state)
            print("✅ Outlet control test completed")
        
        # Disconnect
        print("🔌 Disconnecting...")
        await client.async_disconnect()
        print("✅ Disconnected successfully!")
        
        print("\n🎉 All tests passed! Your device is working correctly.")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False


if __name__ == "__main__":
    success = asyncio.run(test_device())
    sys.exit(0 if success else 1)
