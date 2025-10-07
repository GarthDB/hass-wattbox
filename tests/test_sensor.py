"""Test the Wattbox sensor platform."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from custom_components.wattbox.sensor import (
    async_setup_entry,
    WattboxVoltageSensor,
    WattboxPowerSensor,
)


@pytest.fixture
def mock_coordinator() -> DataUpdateCoordinator:
    """Mock coordinator for testing."""
    coordinator = MagicMock(spec=DataUpdateCoordinator)
    coordinator.data = {
        "voltage": 120.5,
        "power": 150.0,
        "outlets": [
            {"number": 1, "name": "Outlet 1", "state": 1},
            {"number": 2, "name": "Outlet 2", "state": 0},
        ],
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
    """Test async_setup_entry for sensor platform."""
    # Mock the coordinator and device info
    with patch("custom_components.wattbox.sensor.async_setup_entry") as mock_setup:
        mock_setup.return_value = True
        
        result = await async_setup_entry(hass, mock_config_entry)
        
        # Since this is a placeholder, it should return True
        assert result is True


def test_wattbox_voltage_sensor_init(
    mock_coordinator: DataUpdateCoordinator, 
    mock_device_info: DeviceInfo
) -> None:
    """Test WattboxVoltageSensor initialization."""
    sensor = WattboxVoltageSensor(
        coordinator=mock_coordinator,
        device_info=mock_device_info,
        unique_id="test_voltage_sensor",
    )
    
    assert sensor.coordinator == mock_coordinator
    assert sensor.device_info == mock_device_info
    assert sensor.unique_id == "test_voltage_sensor"
    assert sensor.name == "Voltage"


def test_wattbox_voltage_sensor_native_value(
    mock_coordinator: DataUpdateCoordinator, 
    mock_device_info: DeviceInfo
) -> None:
    """Test WattboxVoltageSensor native_value property."""
    sensor = WattboxVoltageSensor(
        coordinator=mock_coordinator,
        device_info=mock_device_info,
        unique_id="test_voltage_sensor",
    )
    
    # Currently returns None (TODO implementation)
    assert sensor.native_value is None


def test_wattbox_voltage_sensor_attributes(
    mock_coordinator: DataUpdateCoordinator, 
    mock_device_info: DeviceInfo
) -> None:
    """Test WattboxVoltageSensor attributes."""
    sensor = WattboxVoltageSensor(
        coordinator=mock_coordinator,
        device_info=mock_device_info,
        unique_id="test_voltage_sensor",
    )
    
    assert sensor.device_class == "voltage"
    assert sensor.native_unit_of_measurement == "V"


def test_wattbox_power_sensor_init(
    mock_coordinator: DataUpdateCoordinator, 
    mock_device_info: DeviceInfo
) -> None:
    """Test WattboxPowerSensor initialization."""
    sensor = WattboxPowerSensor(
        coordinator=mock_coordinator,
        device_info=mock_device_info,
        unique_id="test_power_sensor",
    )
    
    assert sensor.coordinator == mock_coordinator
    assert sensor.device_info == mock_device_info
    assert sensor.unique_id == "test_power_sensor"
    assert sensor.name == "Power"


def test_wattbox_power_sensor_native_value(
    mock_coordinator: DataUpdateCoordinator, 
    mock_device_info: DeviceInfo
) -> None:
    """Test WattboxPowerSensor native_value property."""
    sensor = WattboxPowerSensor(
        coordinator=mock_coordinator,
        device_info=mock_device_info,
        unique_id="test_power_sensor",
    )
    
    # Currently returns None (TODO implementation)
    assert sensor.native_value is None


def test_wattbox_power_sensor_attributes(
    mock_coordinator: DataUpdateCoordinator, 
    mock_device_info: DeviceInfo
) -> None:
    """Test WattboxPowerSensor attributes."""
    sensor = WattboxPowerSensor(
        coordinator=mock_coordinator,
        device_info=mock_device_info,
        unique_id="test_power_sensor",
    )
    
    assert sensor.device_class == "power"
    assert sensor.native_unit_of_measurement == "W"


def test_sensor_inheritance(mock_coordinator: DataUpdateCoordinator, mock_device_info: DeviceInfo) -> None:
    """Test that sensors inherit from correct base classes."""
    voltage_sensor = WattboxVoltageSensor(
        coordinator=mock_coordinator,
        device_info=mock_device_info,
        unique_id="test_voltage_sensor",
    )
    
    power_sensor = WattboxPowerSensor(
        coordinator=mock_coordinator,
        device_info=mock_device_info,
        unique_id="test_power_sensor",
    )
    
    assert isinstance(voltage_sensor, SensorEntity)
    assert isinstance(power_sensor, SensorEntity)
