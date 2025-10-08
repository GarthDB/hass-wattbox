"""Test the Wattbox integration."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from custom_components.wattbox import async_setup_entry, async_unload_entry
from custom_components.wattbox.const import DOMAIN


@pytest.fixture
def mock_config_entry() -> ConfigEntry:
    """Mock config entry for testing."""
    config_entry = MagicMock(spec=ConfigEntry)
    config_entry.version = 1
    config_entry.domain = DOMAIN
    config_entry.title = "Test Wattbox"
    config_entry.data = {
        "host": "192.168.1.100",
        "username": "wattbox",
        "password": "wattbox",
        "polling_interval": 30,
    }
    config_entry.source = "user"
    config_entry.options = {}
    config_entry.entry_id = "test_entry_id"
    return config_entry


@pytest.mark.asyncio
async def test_async_setup_entry(
    hass: HomeAssistant, mock_config_entry: ConfigEntry
) -> None:
    """Test async_setup_entry."""
    with patch(
        "custom_components.wattbox.coordinator.WattboxDataUpdateCoordinator.async_config_entry_first_refresh",
        new_callable=AsyncMock,
    ):
        result = await async_setup_entry(hass, mock_config_entry)

    assert result is True
    assert DOMAIN in hass.data


@pytest.mark.asyncio
async def test_async_unload_entry(
    hass: HomeAssistant, mock_config_entry: ConfigEntry
) -> None:
    """Test async_unload_entry."""
    # First set up the entry
    with patch(
        "custom_components.wattbox.coordinator.WattboxDataUpdateCoordinator.async_config_entry_first_refresh",
        new_callable=AsyncMock,
    ):
        await async_setup_entry(hass, mock_config_entry)

    # Then unload it
    result = await async_unload_entry(hass, mock_config_entry)

    assert result is True


@pytest.mark.asyncio
async def test_async_setup_entry_with_existing_data(
    hass: HomeAssistant, mock_config_entry: ConfigEntry
) -> None:
    """Test async_setup_entry when data already exists."""
    # Pre-populate hass.data
    hass.data[DOMAIN] = {"existing": "data"}

    with patch(
        "custom_components.wattbox.coordinator.WattboxDataUpdateCoordinator.async_config_entry_first_refresh",
        new_callable=AsyncMock,
    ):
        result = await async_setup_entry(hass, mock_config_entry)

    assert result is True
    assert DOMAIN in hass.data
    # Should preserve existing data
    assert "existing" in hass.data[DOMAIN]


@pytest.mark.asyncio
async def test_async_setup_entry_platforms_disabled(
    hass: HomeAssistant, mock_config_entry: ConfigEntry
) -> None:
    """Test async_setup_entry when platforms are disabled (TODO sections)."""
    # The current implementation has TODO sections for platform setup
    # This test verifies it doesn't crash
    with patch(
        "custom_components.wattbox.coordinator.WattboxDataUpdateCoordinator.async_config_entry_first_refresh",
        new_callable=AsyncMock,
    ):
        result = await async_setup_entry(hass, mock_config_entry)

    assert result is True


@pytest.mark.asyncio
async def test_async_unload_entry_platforms_disabled(
    hass: HomeAssistant, mock_config_entry: ConfigEntry
) -> None:
    """Test async_unload_entry when platforms are disabled (TODO sections)."""
    # Set up the data first
    mock_coordinator = MagicMock()
    mock_coordinator.async_disconnect = AsyncMock()
    hass.data[DOMAIN] = {mock_config_entry.entry_id: mock_coordinator}

    # The current implementation has TODO sections for platform unload
    # This test verifies it doesn't crash
    result = await async_unload_entry(hass, mock_config_entry)

    assert result is True
