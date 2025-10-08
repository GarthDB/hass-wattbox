"""Test configuration for Wattbox device testing.

This file contains configuration options for testing with real devices.
DO NOT commit this file to version control with real credentials.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Test device configuration
# Set these via environment variables or create a .env file
# DO NOT hardcode credentials in this file
WATTBOX_TEST_CONFIG = {
    "host": os.getenv("WATTBOX_TEST_HOST", "192.168.1.100"),  # Default example IP
    "username": os.getenv("WATTBOX_TEST_USERNAME", "wattbox"),  # Default example username
    "password": os.getenv("WATTBOX_TEST_PASSWORD", "your_password_here"),  # Set via env var
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
