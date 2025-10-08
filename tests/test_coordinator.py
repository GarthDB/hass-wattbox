"""Test coordinator for Wattbox integration."""

from __future__ import annotations

from datetime import timedelta
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import UpdateFailed

from custom_components.wattbox.coordinator import WattboxDataUpdateCoordinator
from custom_components.wattbox.telnet_client import (
    WattboxAuthenticationError,
    WattboxConnectionError,
    WattboxTelnetClient,
)


@pytest.fixture
def mock_config_entry() -> ConfigEntry:
    """Mock config entry for testing."""
    config_entry = MagicMock(spec=ConfigEntry)
    config_entry.entry_id = "test_entry_id"
    config_entry.data = {
        "host": "192.168.1.100",
        "username": "test_user",
        "password": "test_password",
        "polling_interval": 30,
    }
    return config_entry


@pytest.fixture
def mock_telnet_client() -> WattboxTelnetClient:
    """Mock telnet client for testing."""
    client = MagicMock(spec=WattboxTelnetClient)
    client.is_connected = False
    client.async_connect = AsyncMock()
    client.async_disconnect = AsyncMock()
    client.async_get_device_info = AsyncMock()
    client.async_get_outlet_status = AsyncMock()
    client.async_get_power_metrics = AsyncMock()
    return client


@pytest.fixture
def coordinator(
    hass: HomeAssistant,
    mock_config_entry: ConfigEntry,
    mock_telnet_client: WattboxTelnetClient,
) -> WattboxDataUpdateCoordinator:
    """Create a WattboxDataUpdateCoordinator instance for testing."""
    with patch("homeassistant.helpers.frame.report_usage"):
        return WattboxDataUpdateCoordinator(hass, mock_config_entry, mock_telnet_client)


def test_coordinator_init(
    hass: HomeAssistant,
    mock_config_entry: ConfigEntry,
    mock_telnet_client: WattboxTelnetClient,
) -> None:
    """Test WattboxDataUpdateCoordinator initialization."""
    with patch("homeassistant.helpers.frame.report_usage"):
        coordinator = WattboxDataUpdateCoordinator(
            hass, mock_config_entry, mock_telnet_client
        )

    assert coordinator.telnet_client == mock_telnet_client
    assert coordinator.update_interval == timedelta(seconds=30)


def test_coordinator_init_custom_polling_interval(
    hass: HomeAssistant,
    mock_telnet_client: WattboxTelnetClient,
) -> None:
    """Test coordinator initialization with custom polling interval."""
    config_entry = MagicMock(spec=ConfigEntry)
    config_entry.data = {"polling_interval": 60}

    with patch("homeassistant.helpers.frame.report_usage"):
        coordinator = WattboxDataUpdateCoordinator(
            hass, config_entry, mock_telnet_client
        )

    assert coordinator.update_interval == timedelta(seconds=60)


@pytest.mark.asyncio
async def test_async_update_data_success(
    coordinator: WattboxDataUpdateCoordinator,
    mock_telnet_client: WattboxTelnetClient,
) -> None:
    """Test successful data update."""
    # Mock successful data retrieval
    mock_telnet_client.async_get_device_info.return_value = {
        "hardware_version": "1.0.0",
        "model": "WB-800VPS-IPVM-18",
        "serial_number": "TEST123",
        "hostname": "test-wattbox",
    }

    mock_telnet_client.async_get_outlet_status.return_value = [
        {"state": 1, "name": "Outlet 1"},
        {"state": 0, "name": "Outlet 2"},
    ]

    mock_telnet_client.async_get_power_metrics.return_value = {
        "voltage": 120.5,
        "current": 1.2,
        "power": 144.6,
    }

    data = await coordinator._async_update_data()

    assert data["connected"] is True
    assert data["device_info"]["hostname"] == "test-wattbox"
    assert len(data["outlet_info"]) == 2
    assert data["voltage"] == 120.5
    assert data["current"] == 1.2
    assert data["power"] == 144.6

    # Verify client methods were called
    mock_telnet_client.async_connect.assert_called_once()
    mock_telnet_client.async_get_device_info.assert_called_once()
    mock_telnet_client.async_get_outlet_status.assert_called_once_with(18)
    mock_telnet_client.async_get_power_metrics.assert_called_once()


@pytest.mark.asyncio
async def test_async_update_data_connection_error(
    coordinator: WattboxDataUpdateCoordinator,
    mock_telnet_client: WattboxTelnetClient,
) -> None:
    """Test data update with connection error."""
    mock_telnet_client.async_connect.side_effect = WattboxConnectionError(
        "Connection failed"
    )

    with pytest.raises(UpdateFailed, match="Connection error: Connection failed"):
        await coordinator._async_update_data()


@pytest.mark.asyncio
async def test_async_update_data_authentication_error(
    coordinator: WattboxDataUpdateCoordinator,
    mock_telnet_client: WattboxTelnetClient,
) -> None:
    """Test data update with authentication error."""
    mock_telnet_client.async_connect.side_effect = WattboxAuthenticationError(
        "Auth failed"
    )

    with pytest.raises(UpdateFailed, match="Unexpected error: Auth failed"):
        await coordinator._async_update_data()


@pytest.mark.asyncio
async def test_async_update_data_general_error(
    coordinator: WattboxDataUpdateCoordinator,
    mock_telnet_client: WattboxTelnetClient,
) -> None:
    """Test data update with general error."""
    mock_telnet_client.async_connect.side_effect = Exception("Unknown error")

    with pytest.raises(UpdateFailed, match="Unexpected error: Unknown error"):
        await coordinator._async_update_data()


@pytest.mark.asyncio
async def test_async_set_outlet_state(
    coordinator: WattboxDataUpdateCoordinator,
    mock_telnet_client: WattboxTelnetClient,
) -> None:
    """Test setting outlet state."""
    mock_telnet_client.async_set_outlet_state = AsyncMock()
    coordinator.async_request_refresh = AsyncMock()

    await coordinator.async_set_outlet_state(1, True)

    mock_telnet_client.async_set_outlet_state.assert_called_once_with(1, True)
    coordinator.async_request_refresh.assert_called_once()


@pytest.mark.asyncio
async def test_async_disconnect(
    coordinator: WattboxDataUpdateCoordinator,
    mock_telnet_client: WattboxTelnetClient,
) -> None:
    """Test disconnecting the client."""
    await coordinator.async_disconnect()

    mock_telnet_client.async_disconnect.assert_called_once()


@pytest.mark.asyncio
async def test_async_update_data_already_connected(
    coordinator: WattboxDataUpdateCoordinator,
    mock_telnet_client: WattboxTelnetClient,
) -> None:
    """Test data update when already connected."""
    # Set client as already connected
    mock_telnet_client.is_connected = True

    # Mock successful data retrieval
    mock_telnet_client.async_get_device_info.return_value = {
        "hardware_version": "1.0.0",
        "model": "WB-800VPS-IPVM-18",
        "serial_number": "TEST123",
        "hostname": "test-wattbox",
    }

    mock_telnet_client.async_get_outlet_status.return_value = []
    mock_telnet_client.async_get_power_metrics.return_value = {
        "voltage": None,
        "current": None,
        "power": None,
    }

    data = await coordinator._async_update_data()

    assert data["connected"] is True
    # Should not call async_connect since already connected
    mock_telnet_client.async_connect.assert_not_called()


@pytest.mark.asyncio
async def test_async_update_data_outlet_info_error(
    coordinator: WattboxDataUpdateCoordinator,
    mock_telnet_client: WattboxTelnetClient,
) -> None:
    """Test data update with outlet info error."""
    # Mock successful connection and device info
    mock_telnet_client.async_get_device_info.return_value = {
        "hardware_version": "1.0.0",
        "model": "WB-800VPS-IPVM-18",
        "serial_number": "TEST123",
        "hostname": "test-wattbox",
    }

    # Mock outlet status error
    mock_telnet_client.async_get_outlet_status.side_effect = Exception("Outlet error")

    mock_telnet_client.async_get_power_metrics.return_value = {
        "voltage": None,
        "current": None,
        "power": None,
    }

    with pytest.raises(UpdateFailed, match="Unexpected error: Outlet error"):
        await coordinator._async_update_data()


@pytest.mark.asyncio
async def test_async_update_data_power_metrics_error(
    coordinator: WattboxDataUpdateCoordinator,
    mock_telnet_client: WattboxTelnetClient,
) -> None:
    """Test data update with power metrics error."""
    # Mock successful connection, device info, and outlet status
    mock_telnet_client.async_get_device_info.return_value = {
        "hardware_version": "1.0.0",
        "model": "WB-800VPS-IPVM-18",
        "serial_number": "TEST123",
        "hostname": "test-wattbox",
    }

    mock_telnet_client.async_get_outlet_status.return_value = []

    # Mock power metrics error
    mock_telnet_client.async_get_power_metrics.side_effect = Exception("Power error")

    with pytest.raises(UpdateFailed, match="Unexpected error: Power error"):
        await coordinator._async_update_data()
