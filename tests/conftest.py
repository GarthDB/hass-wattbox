"""Test configuration for Wattbox integration."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest
import pytest_asyncio
from homeassistant.core import HomeAssistant

from custom_components.wattbox.const import DOMAIN


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
    hass.entity_registry = MagicMock()
    hass.device_registry = MagicMock()

    # Start the Home Assistant instance
    await hass.async_start()

    yield hass

    # Clean up
    await hass.async_stop()
    loop.close()
