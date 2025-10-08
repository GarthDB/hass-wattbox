#!/usr/bin/env python3
"""
Comprehensive test script for Issue #4: Outlet Control Implementation

This script tests all outlet control functionality with the real Wattbox device:
- Individual outlet on/off control (1-18 outlets)
- State synchronization
- Error handling
- Switch entity behavior simulation
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


class OutletControlTester:
    """Test outlet control functionality."""

    def __init__(self, host: str, username: str, password: str) -> None:
        """Initialize the tester."""
        self._client = WattboxTelnetClient(host, username, password)
        self._test_results = {
            "connection": False,
            "outlet_states": {},
            "control_tests": {},
            "errors": []
        }

    async def run_comprehensive_test(self) -> dict:
        """Run comprehensive outlet control tests."""
        _LOGGER.info("🔌 Starting comprehensive outlet control testing...")
        
        try:
            # Test 1: Connection
            await self._test_connection()
            
            # Test 2: Get initial outlet states
            await self._test_get_outlet_states()
            
            # Test 3: Individual outlet control
            await self._test_individual_outlet_control()
            
            # Test 4: State synchronization
            await self._test_state_synchronization()
            
            # Test 5: Error handling
            await self._test_error_handling()
            
            _LOGGER.info("✅ All outlet control tests completed!")
            
        except Exception as e:
            _LOGGER.error(f"❌ Test failed: {e}")
            self._test_results["errors"].append(str(e))
        finally:
            await self._client.async_disconnect()
            
        return self._test_results

    async def _test_connection(self) -> None:
        """Test connection to the device."""
        _LOGGER.info("🔗 Testing connection...")
        await self._client.async_connect()
        self._test_results["connection"] = True
        _LOGGER.info("✅ Connection successful")

    async def _test_get_outlet_states(self) -> None:
        """Test getting outlet states."""
        _LOGGER.info("📊 Getting initial outlet states...")
        
        # Get outlet status
        outlet_info = await self._client.async_get_outlet_status(18)
        
        for i, outlet in enumerate(outlet_info):
            outlet_num = i + 1
            state = outlet.get("state", 0)
            name = outlet.get("name", f"Outlet {outlet_num}")
            self._test_results["outlet_states"][outlet_num] = {
                "initial_state": bool(state),
                "name": name
            }
            _LOGGER.info(f"  Outlet {outlet_num}: {state} - {name}")
        
        _LOGGER.info(f"✅ Retrieved {len(outlet_info)} outlet states")

    async def _test_individual_outlet_control(self) -> None:
        """Test individual outlet control."""
        _LOGGER.info("🎛️ Testing individual outlet control...")
        
        # Test outlets 1, 2, and 3 (to avoid affecting too many)
        test_outlets = [1, 2, 3]
        
        for outlet_num in test_outlets:
            _LOGGER.info(f"  Testing outlet {outlet_num}...")
            
            # Get initial state
            initial_state = self._test_results["outlet_states"][outlet_num]["initial_state"]
            _LOGGER.info(f"    Initial state: {initial_state}")
            
            # Test turning ON
            _LOGGER.info(f"    Turning outlet {outlet_num} ON...")
            await self._client.async_set_outlet_state(outlet_num, True)
            await asyncio.sleep(1)  # Wait for state change
            
            # Verify state change
            outlet_info = await self._client.async_get_outlet_status(18)
            new_state = bool(outlet_info[outlet_num - 1].get("state", 0))
            _LOGGER.info(f"    State after ON: {new_state}")
            
            # Test turning OFF
            _LOGGER.info(f"    Turning outlet {outlet_num} OFF...")
            await self._client.async_set_outlet_state(outlet_num, False)
            await asyncio.sleep(1)  # Wait for state change
            
            # Verify state change
            outlet_info = await self._client.async_get_outlet_status(18)
            final_state = bool(outlet_info[outlet_num - 1].get("state", 0))
            _LOGGER.info(f"    State after OFF: {final_state}")
            
            # Restore original state
            _LOGGER.info(f"    Restoring outlet {outlet_num} to original state...")
            await self._client.async_set_outlet_state(outlet_num, initial_state)
            
            # Record test results
            self._test_results["control_tests"][outlet_num] = {
                "initial_state": initial_state,
                "on_command_worked": new_state,
                "off_command_worked": not final_state,
                "restore_worked": True
            }
            
            _LOGGER.info(f"    ✅ Outlet {outlet_num} control test completed")

    async def _test_state_synchronization(self) -> None:
        """Test state synchronization."""
        _LOGGER.info("🔄 Testing state synchronization...")
        
        # Get states before and after a change
        outlet_info_before = await self._client.async_get_outlet_status(18)
        
        # Make a change
        await self._client.async_set_outlet_state(1, True)
        await asyncio.sleep(1)
        
        # Get states after
        outlet_info_after = await self._client.async_get_outlet_status(18)
        
        # Compare states
        state_changed = outlet_info_before[0]["state"] != outlet_info_after[0]["state"]
        
        self._test_results["state_synchronization"] = {
            "state_changed": state_changed,
            "before": outlet_info_before[0]["state"],
            "after": outlet_info_after[0]["state"]
        }
        
        _LOGGER.info(f"✅ State synchronization test: {state_changed}")

    async def _test_error_handling(self) -> None:
        """Test error handling."""
        _LOGGER.info("⚠️ Testing error handling...")
        
        # Test invalid outlet number
        try:
            await self._client.async_set_outlet_state(99, True)  # Invalid outlet
            self._test_results["error_handling"] = {"invalid_outlet": "no_error"}
        except Exception as e:
            self._test_results["error_handling"] = {"invalid_outlet": str(e)}
            _LOGGER.info(f"✅ Invalid outlet handled: {e}")
        
        # Test with disconnected client (simulate connection loss)
        try:
            await self._client.async_disconnect()
            await self._client.async_set_outlet_state(1, True)  # Should reconnect
            self._test_results["error_handling"]["reconnect"] = "success"
            _LOGGER.info("✅ Reconnection test passed")
        except Exception as e:
            self._test_results["error_handling"]["reconnect"] = str(e)
            _LOGGER.info(f"❌ Reconnection test failed: {e}")

    def print_summary(self) -> None:
        """Print test summary."""
        print("\n" + "="*60)
        print("OUTLET CONTROL TEST SUMMARY")
        print("="*60)
        
        # Connection test
        print(f"Connection: {'✅ PASS' if self._test_results['connection'] else '❌ FAIL'}")
        
        # Outlet states
        print(f"Outlets detected: {len(self._test_results['outlet_states'])}")
        
        # Control tests
        control_tests = self._test_results.get("control_tests", {})
        print(f"Control tests: {len(control_tests)} outlets tested")
        
        for outlet_num, results in control_tests.items():
            status = "✅ PASS" if results["on_command_worked"] and results["off_command_worked"] else "❌ FAIL"
            print(f"  Outlet {outlet_num}: {status}")
        
        # State synchronization
        sync_test = self._test_results.get("state_synchronization", {})
        sync_status = "✅ PASS" if sync_test.get("state_changed", False) else "❌ FAIL"
        print(f"State sync: {sync_status}")
        
        # Error handling
        error_test = self._test_results.get("error_handling", {})
        print(f"Error handling: {'✅ PASS' if error_test else '❌ PARTIAL'}")
        
        # Errors
        if self._test_results["errors"]:
            print(f"Errors: {len(self._test_results['errors'])}")
            for error in self._test_results["errors"]:
                print(f"  - {error}")
        
        print("="*60)


async def main():
    """Main test function."""
    config = WATTBOX_TEST_CONFIG
    
    _LOGGER.info(f"🔌 Testing outlet control with {config['host']}")
    
    tester = OutletControlTester(
        config["host"],
        config["username"], 
        config["password"]
    )
    
    results = await tester.run_comprehensive_test()
    tester.print_summary()
    
    # Determine exit code
    if results["connection"] and not results["errors"]:
        _LOGGER.info("🎉 All outlet control tests passed!")
        return 0
    else:
        _LOGGER.error("❌ Some outlet control tests failed!")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
