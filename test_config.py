"""Test configuration for Wattbox device testing.

This file contains configuration options for testing with real devices.
DO NOT commit this file to version control with real credentials.
"""

import os
from pathlib import Path

# Test device configuration
# You can set these via environment variables or edit this file directly
WATTBOX_TEST_CONFIG = {
    "host": os.getenv("WATTBOX_TEST_HOST", "192.168.1.34"),  # Your actual device IP
    "username": os.getenv("WATTBOX_TEST_USERNAME", "garthdb"),
    "password": os.getenv("WATTBOX_TEST_PASSWORD", "FE@7bc3YHE86q!cb"),
    "port": int(os.getenv("WATTBOX_TEST_PORT", "23")),
    "timeout": int(os.getenv("WATTBOX_TEST_TIMEOUT", "10")),
    "scan_interval": int(os.getenv("WATTBOX_TEST_SCAN_INTERVAL", "20")),  # seconds
}

# Test settings
TEST_SETTINGS = {
    "capture_data": True,  # Whether to capture real device data
    "test_outlet_control": False,  # Whether to test outlet control (safety)
    "outlet_to_test": 1,  # Which outlet to test (if testing outlet control)
    "save_fixtures": True,  # Whether to save captured data as test fixtures
}

# File paths
TEST_DIR = Path(__file__).parent
FIXTURES_DIR = TEST_DIR / "fixtures"
CAPTURED_DATA_FILE = FIXTURES_DIR / "real_device_data.json"
