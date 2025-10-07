"""Test configuration for Wattbox integration."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest
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


@pytest.fixture
def hass() -> HomeAssistant:
    """Return a Home Assistant instance."""
    from homeassistant.core import HomeAssistant
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.helpers.entity_registry import EntityRegistry
    from homeassistant.helpers.device_registry import DeviceRegistry

    hass = HomeAssistant("")
    hass.config_entries = MagicMock()
    hass.entity_registry = MagicMock()
    hass.device_registry = MagicMock()
    return hass
