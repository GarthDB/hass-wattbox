"""Test the Wattbox binary sensor platform."""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest
from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from custom_components.wattbox.binary_sensor import (
    WattboxPowerLostBinarySensor,
    WattboxSafeVoltageBinarySensor,
    WattboxStatusBinarySensor,
    WattboxUPSConnectedBinarySensor,
    WattboxUPSPowerLostBinarySensor,
    async_setup_entry,
)
from custom_components.wattbox.const import DOMAIN


@pytest.fixture
def mock_coordinator() -> DataUpdateCoordinator:
    """Mock coordinator for testing."""
    coordinator = MagicMock(spec=DataUpdateCoordinator)
    coordinator.data = {
        "connected": True,
        "last_update": "2023-01-01T00:00:00Z",
    }
    return coordinator


@pytest.fixture
def mock_device_info() -> DeviceInfo:
    """Mock device info for testing."""
    return DeviceInfo(
        identifiers={("wattbox", "test_device")},
        name="Test Wattbox",
        manufacturer="SnapAV",
        model="WB-800VPS-IPVM-18",
        sw_version="1.0.0",
    )


@pytest.fixture
def mock_config_entry() -> ConfigEntry:
    """Mock config entry for testing."""
    config_entry = MagicMock(spec=ConfigEntry)
    config_entry.version = 1
    config_entry.domain = "wattbox"
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
    hass: HomeAssistant,
    mock_config_entry: ConfigEntry,
    mock_coordinator: DataUpdateCoordinator,
    mock_device_info: DeviceInfo,
) -> None:
    """Test async_setup_entry for binary sensor platform."""
    # Mock the coordinator in hass.data
    hass.data[DOMAIN] = {mock_config_entry.entry_id: mock_coordinator}

    # Create a mock async_add_entities function
    async def mock_add_entities(entities):
        pass

    result = await async_setup_entry(hass, mock_config_entry, mock_add_entities)

    # Should return None (no return value)
    assert result is None


def test_wattbox_status_binary_sensor_init(
    mock_coordinator: DataUpdateCoordinator, mock_device_info: DeviceInfo
) -> None:
    """Test WattboxStatusBinarySensor initialization."""
    sensor = WattboxStatusBinarySensor(
        coordinator=mock_coordinator,
        entry_id="test_entry_id",
    )

    assert sensor.coordinator == mock_coordinator
    assert sensor.unique_id == "test_entry_id_status"
    assert sensor.name == "Device Status"


def test_wattbox_status_binary_sensor_is_on(
    mock_coordinator: DataUpdateCoordinator, mock_device_info: DeviceInfo
) -> None:
    """Test WattboxStatusBinarySensor is_on property."""
    sensor = WattboxStatusBinarySensor(
        coordinator=mock_coordinator,
        entry_id="test_entry_id",
    )

    # Test when device is connected
    mock_coordinator.data = {"connected": True}
    assert sensor.is_on is True

    # Test when device is not connected
    mock_coordinator.data = {"connected": False}
    assert sensor.is_on is False

    # Test when no connection data
    mock_coordinator.data = {}
    assert sensor.is_on is False


def test_wattbox_status_binary_sensor_attributes(
    mock_coordinator: DataUpdateCoordinator, mock_device_info: DeviceInfo
) -> None:
    """Test WattboxStatusBinarySensor attributes."""
    sensor = WattboxStatusBinarySensor(
        coordinator=mock_coordinator,
        entry_id="test_entry_id",
    )

    assert sensor.device_class == "connectivity"


def test_binary_sensor_inheritance(
    mock_coordinator: DataUpdateCoordinator, mock_device_info: DeviceInfo
) -> None:
    """Test that binary sensors inherit from correct base classes."""
    sensor = WattboxStatusBinarySensor(
        coordinator=mock_coordinator,
        entry_id="test_entry_id",
    )

    assert isinstance(sensor, BinarySensorEntity)


def test_wattbox_status_binary_sensor_name(
    mock_coordinator: DataUpdateCoordinator, mock_device_info: DeviceInfo
) -> None:
    """Test WattboxStatusBinarySensor name property."""
    sensor = WattboxStatusBinarySensor(
        coordinator=mock_coordinator,
        entry_id="test_entry_id",
    )

    assert sensor.name == "Device Status"


def test_wattbox_status_binary_sensor_device_class(
    mock_coordinator: DataUpdateCoordinator, mock_device_info: DeviceInfo
) -> None:
    """Test WattboxStatusBinarySensor device_class property."""
    sensor = WattboxStatusBinarySensor(
        coordinator=mock_coordinator,
        entry_id="test_entry_id",
    )

    assert sensor.device_class == "connectivity"


# Tests for WattboxPowerLostBinarySensor
def test_wattbox_power_lost_binary_sensor_init(
    mock_coordinator: DataUpdateCoordinator, mock_device_info: DeviceInfo
) -> None:
    """Test WattboxPowerLostBinarySensor initialization."""
    sensor = WattboxPowerLostBinarySensor(
        coordinator=mock_coordinator,
        entry_id="test_entry_id",
    )

    assert sensor.coordinator == mock_coordinator
    assert sensor.unique_id == "test_entry_id_power_lost"
    assert sensor.name == "Power Lost"
    assert sensor.device_class == "power"


def test_wattbox_power_lost_binary_sensor_is_on(
    mock_coordinator: DataUpdateCoordinator, mock_device_info: DeviceInfo
) -> None:
    """Test WattboxPowerLostBinarySensor is_on property."""
    sensor = WattboxPowerLostBinarySensor(
        coordinator=mock_coordinator,
        entry_id="test_entry_id",
    )

    # Test when power is lost
    mock_coordinator.data = {"status_info": {"ups_status": {"power_lost": True}}}
    assert sensor.is_on is True

    # Test when power is not lost
    mock_coordinator.data = {"status_info": {"ups_status": {"power_lost": False}}}
    assert sensor.is_on is False

    # Test when no status data
    mock_coordinator.data = {}
    assert sensor.is_on is False


# Tests for WattboxSafeVoltageBinarySensor
def test_wattbox_safe_voltage_binary_sensor_init(
    mock_coordinator: DataUpdateCoordinator, mock_device_info: DeviceInfo
) -> None:
    """Test WattboxSafeVoltageBinarySensor initialization."""
    sensor = WattboxSafeVoltageBinarySensor(
        coordinator=mock_coordinator,
        entry_id="test_entry_id",
    )

    assert sensor.coordinator == mock_coordinator
    assert sensor.unique_id == "test_entry_id_safe_voltage"
    assert sensor.name == "Safe Voltage"
    assert sensor.device_class == "voltage"


def test_wattbox_safe_voltage_binary_sensor_is_on(
    mock_coordinator: DataUpdateCoordinator, mock_device_info: DeviceInfo
) -> None:
    """Test WattboxSafeVoltageBinarySensor is_on property."""
    sensor = WattboxSafeVoltageBinarySensor(
        coordinator=mock_coordinator,
        entry_id="test_entry_id",
    )

    # Test when voltage is safe (1)
    mock_coordinator.data = {"status_info": {"power_status": {"safe_voltage": 1}}}
    assert sensor.is_on is True

    # Test when voltage is not safe (0)
    mock_coordinator.data = {"status_info": {"power_status": {"safe_voltage": 0}}}
    assert sensor.is_on is False

    # Test when no status data
    mock_coordinator.data = {}
    assert sensor.is_on is None


# Tests for WattboxUPSConnectedBinarySensor
def test_wattbox_ups_connected_binary_sensor_init(
    mock_coordinator: DataUpdateCoordinator, mock_device_info: DeviceInfo
) -> None:
    """Test WattboxUPSConnectedBinarySensor initialization."""
    sensor = WattboxUPSConnectedBinarySensor(
        coordinator=mock_coordinator,
        entry_id="test_entry_id",
    )

    assert sensor.coordinator == mock_coordinator
    assert sensor.unique_id == "test_entry_id_ups_connected"
    assert sensor.name == "UPS Connected"
    assert sensor.device_class == "connectivity"


def test_wattbox_ups_connected_binary_sensor_is_on(
    mock_coordinator: DataUpdateCoordinator, mock_device_info: DeviceInfo
) -> None:
    """Test WattboxUPSConnectedBinarySensor is_on property."""
    sensor = WattboxUPSConnectedBinarySensor(
        coordinator=mock_coordinator,
        entry_id="test_entry_id",
    )

    # Test when UPS is connected
    mock_coordinator.data = {"status_info": {"ups_connected": True}}
    assert sensor.is_on is True

    # Test when UPS is not connected
    mock_coordinator.data = {"status_info": {"ups_connected": False}}
    assert sensor.is_on is False

    # Test when no status data
    mock_coordinator.data = {}
    assert sensor.is_on is False


# Tests for WattboxUPSPowerLostBinarySensor
def test_wattbox_ups_power_lost_binary_sensor_init(
    mock_coordinator: DataUpdateCoordinator, mock_device_info: DeviceInfo
) -> None:
    """Test WattboxUPSPowerLostBinarySensor initialization."""
    sensor = WattboxUPSPowerLostBinarySensor(
        coordinator=mock_coordinator,
        entry_id="test_entry_id",
    )

    assert sensor.coordinator == mock_coordinator
    assert sensor.unique_id == "test_entry_id_ups_power_lost"
    assert sensor.name == "UPS Power Lost"
    assert sensor.device_class == "power"


def test_wattbox_ups_power_lost_binary_sensor_is_on(
    mock_coordinator: DataUpdateCoordinator, mock_device_info: DeviceInfo
) -> None:
    """Test WattboxUPSPowerLostBinarySensor is_on property."""
    sensor = WattboxUPSPowerLostBinarySensor(
        coordinator=mock_coordinator,
        entry_id="test_entry_id",
    )

    # Test when UPS power is lost
    mock_coordinator.data = {"status_info": {"ups_status": {"power_lost": True}}}
    assert sensor.is_on is True

    # Test when UPS power is not lost
    mock_coordinator.data = {"status_info": {"ups_status": {"power_lost": False}}}
    assert sensor.is_on is False

    # Test when no status data
    mock_coordinator.data = {}
    assert sensor.is_on is False
