"""Test configuration for Wattbox integration."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest
import pytest_asyncio

# Mock Home Assistant imports for CI testing
try:
    from homeassistant.core import HomeAssistant
except ImportError:
    # Use our mock Home Assistant module
    import sys

    from .mock_homeassistant import homeassistant

    sys.modules["homeassistant"] = homeassistant
    sys.modules["homeassistant.core"] = homeassistant.core
    sys.modules["homeassistant.config_entries"] = homeassistant.config_entries
    sys.modules["homeassistant.data_entry_flow"] = homeassistant.data_entry_flow
    sys.modules["homeassistant.helpers.entity"] = homeassistant.helpers.entity
    sys.modules["homeassistant.helpers.update_coordinator"] = (
        homeassistant.helpers.update_coordinator
    )
    sys.modules["homeassistant.components.binary_sensor"] = (
        homeassistant.components.binary_sensor
    )
    sys.modules["homeassistant.components.sensor"] = homeassistant.components.sensor
    sys.modules["homeassistant.components.switch"] = homeassistant.components.switch
    # Add missing modules that our code imports
    sys.modules["homeassistant.const"] = homeassistant.const
    sys.modules["homeassistant.helpers"] = homeassistant.helpers
    sys.modules["homeassistant.helpers.frame"] = homeassistant.helpers.frame

    from homeassistant.core import HomeAssistant

from custom_components.wattbox.const import DOMAIN

# Note: We don't need to patch report_usage as it's not essential for our tests


@pytest.fixture
def mock_coordinator():
    """Mock coordinator for testing."""
    coordinator = MagicMock()
    coordinator.data = {}
    coordinator.async_request_refresh = AsyncMock()
    return coordinator


@pytest.fixture
def mock_device_info():
    """Mock device info for testing."""
    return {
        "identifiers": {(DOMAIN, "test_device")},
        "name": "Test Wattbox",
        "manufacturer": "SnapAV",
        "model": "WB-800VPS-IPVM-18",
    }


@pytest_asyncio.fixture
async def hass() -> HomeAssistant:
    """Return a Home Assistant instance."""
    import asyncio

    # Create a new event loop for this test
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    hass = HomeAssistant("")
    hass.config_entries = MagicMock()
    hass.config_entries.async_unload_platforms = AsyncMock(return_value=True)
    hass.config_entries.async_forward_entry_setups = AsyncMock(return_value=None)
    hass.entity_registry = MagicMock()
    hass.device_registry = MagicMock()

    # Mock the config entries flow
    hass.config_entries.flow = MagicMock()
    hass.config_entries.flow.async_init = AsyncMock()

    # Start the Home Assistant instance
    await hass.async_start()

    yield hass

    # Clean up
    await hass.async_stop()
    loop.close()
