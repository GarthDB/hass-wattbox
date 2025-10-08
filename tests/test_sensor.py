"""Test sensor platform for Wattbox integration."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from custom_components.wattbox.sensor import (
    WattboxCurrentSensor,
    WattboxFirmwareSensor,
    WattboxHostnameSensor,
    WattboxModelSensor,
    WattboxPowerSensor,
    WattboxSerialSensor,
    WattboxVoltageSensor,
    async_setup_entry,
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
def mock_coordinator() -> DataUpdateCoordinator:
    """Mock coordinator for testing."""
    coordinator = MagicMock(spec=DataUpdateCoordinator)
    coordinator.data = {
        "device_info": {
            "hardware_version": "1.0.0",
            "model": "WB-800VPS-IPVM-18",
            "serial_number": "TEST123",
            "hostname": "test-wattbox",
        },
        "voltage": 120.5,
        "current": 1.2,
        "power": 144.6,
    }
    return coordinator


@pytest.mark.asyncio
async def test_async_setup_entry(
    hass: HomeAssistant,
    mock_config_entry: ConfigEntry,
    mock_coordinator: DataUpdateCoordinator,
) -> None:
    """Test async_setup_entry for sensor platform."""
    # Ensure coordinator has proper data structure
    mock_coordinator.data = {
        "device_info": {
            "hardware_version": "1.0.0",
            "model": "WB-800VPS-IPVM-18",
            "serial_number": "TEST123",
            "hostname": "test-wattbox",
        },
        "voltage": 120.5,
        "current": 1.2,
        "power": 144.6,
    }
    
    # Mock the coordinator in hass.data
    hass.data["wattbox"] = {mock_config_entry.entry_id: mock_coordinator}
    
    # Create a mock async_add_entities function
    entities_added = []
    async def mock_add_entities(entities):
        entities_added.extend(entities)

    result = await async_setup_entry(hass, mock_config_entry, mock_add_entities)

    # Should return None (no return value)
    assert result is None
    
    # Should have created 7 sensors (4 device info + 3 power monitoring)
    assert len(entities_added) == 7


def test_wattbox_firmware_sensor_init(
    mock_coordinator: DataUpdateCoordinator,
) -> None:
    """Test WattboxFirmwareSensor initialization."""
    sensor = WattboxFirmwareSensor(
        coordinator=mock_coordinator,
        entry_id="test_entry_id",
    )

    assert sensor.coordinator == mock_coordinator
    assert sensor.unique_id == "test_entry_id_firmware"
    assert sensor.name == "Firmware"
    assert sensor.device_class is None


def test_wattbox_firmware_sensor_native_value(
    mock_coordinator: DataUpdateCoordinator,
) -> None:
    """Test WattboxFirmwareSensor native_value property."""
    sensor = WattboxFirmwareSensor(
        coordinator=mock_coordinator,
        entry_id="test_entry_id",
    )

    # Test with data
    assert sensor.native_value == "1.0.0"

    # Test without data
    mock_coordinator.data = {}
    assert sensor.native_value is None


def test_wattbox_model_sensor_init(
    mock_coordinator: DataUpdateCoordinator,
) -> None:
    """Test WattboxModelSensor initialization."""
    sensor = WattboxModelSensor(
        coordinator=mock_coordinator,
        entry_id="test_entry_id",
    )

    assert sensor.coordinator == mock_coordinator
    assert sensor.unique_id == "test_entry_id_model"
    assert sensor.name == "Model"
    assert sensor.device_class is None


def test_wattbox_model_sensor_native_value(
    mock_coordinator: DataUpdateCoordinator,
) -> None:
    """Test WattboxModelSensor native_value property."""
    sensor = WattboxModelSensor(
        coordinator=mock_coordinator,
        entry_id="test_entry_id",
    )

    # Test with data
    assert sensor.native_value == "WB-800VPS-IPVM-18"

    # Test without data
    mock_coordinator.data = {}
    assert sensor.native_value is None


def test_wattbox_serial_sensor_init(
    mock_coordinator: DataUpdateCoordinator,
) -> None:
    """Test WattboxSerialSensor initialization."""
    sensor = WattboxSerialSensor(
        coordinator=mock_coordinator,
        entry_id="test_entry_id",
    )

    assert sensor.coordinator == mock_coordinator
    assert sensor.unique_id == "test_entry_id_serial"
    assert sensor.name == "Serial Number"
    assert sensor.device_class is None


def test_wattbox_serial_sensor_native_value(
    mock_coordinator: DataUpdateCoordinator,
) -> None:
    """Test WattboxSerialSensor native_value property."""
    sensor = WattboxSerialSensor(
        coordinator=mock_coordinator,
        entry_id="test_entry_id",
    )

    # Test with data
    assert sensor.native_value == "TEST123"

    # Test without data
    mock_coordinator.data = {}
    assert sensor.native_value is None


def test_wattbox_hostname_sensor_init(
    mock_coordinator: DataUpdateCoordinator,
) -> None:
    """Test WattboxHostnameSensor initialization."""
    sensor = WattboxHostnameSensor(
        coordinator=mock_coordinator,
        entry_id="test_entry_id",
    )

    assert sensor.coordinator == mock_coordinator
    assert sensor.unique_id == "test_entry_id_hostname"
    assert sensor.name == "Hostname"
    assert sensor.device_class is None


def test_wattbox_hostname_sensor_native_value(
    mock_coordinator: DataUpdateCoordinator,
) -> None:
    """Test WattboxHostnameSensor native_value property."""
    sensor = WattboxHostnameSensor(
        coordinator=mock_coordinator,
        entry_id="test_entry_id",
    )

    # Test with data
    assert sensor.native_value == "test-wattbox"

    # Test without data
    mock_coordinator.data = {}
    assert sensor.native_value is None


def test_wattbox_voltage_sensor_init(
    mock_coordinator: DataUpdateCoordinator,
) -> None:
    """Test WattboxVoltageSensor initialization."""
    sensor = WattboxVoltageSensor(
        coordinator=mock_coordinator,
        entry_id="test_entry_id",
    )

    assert sensor.coordinator == mock_coordinator
    assert sensor.unique_id == "test_entry_id_voltage"
    assert sensor.name == "Voltage"
    assert sensor.device_class == "voltage"
    assert sensor.native_unit_of_measurement == "V"


def test_wattbox_voltage_sensor_native_value(
    mock_coordinator: DataUpdateCoordinator,
) -> None:
    """Test WattboxVoltageSensor native_value property."""
    sensor = WattboxVoltageSensor(
        coordinator=mock_coordinator,
        entry_id="test_entry_id",
    )

    # Test with data
    assert sensor.native_value == 120.5

    # Test without data
    mock_coordinator.data = {}
    assert sensor.native_value is None


def test_wattbox_current_sensor_init(
    mock_coordinator: DataUpdateCoordinator,
) -> None:
    """Test WattboxCurrentSensor initialization."""
    sensor = WattboxCurrentSensor(
        coordinator=mock_coordinator,
        entry_id="test_entry_id",
    )

    assert sensor.coordinator == mock_coordinator
    assert sensor.unique_id == "test_entry_id_current"
    assert sensor.name == "Current"
    assert sensor.device_class == "current"
    assert sensor.native_unit_of_measurement == "A"


def test_wattbox_current_sensor_native_value(
    mock_coordinator: DataUpdateCoordinator,
) -> None:
    """Test WattboxCurrentSensor native_value property."""
    sensor = WattboxCurrentSensor(
        coordinator=mock_coordinator,
        entry_id="test_entry_id",
    )

    # Test with data
    assert sensor.native_value == 1.2

    # Test without data
    mock_coordinator.data = {}
    assert sensor.native_value is None


def test_wattbox_power_sensor_init(
    mock_coordinator: DataUpdateCoordinator,
) -> None:
    """Test WattboxPowerSensor initialization."""
    sensor = WattboxPowerSensor(
        coordinator=mock_coordinator,
        entry_id="test_entry_id",
    )

    assert sensor.coordinator == mock_coordinator
    assert sensor.unique_id == "test_entry_id_power"
    assert sensor.name == "Power"
    assert sensor.device_class == "power"
    assert sensor.native_unit_of_measurement == "W"


def test_wattbox_power_sensor_native_value(
    mock_coordinator: DataUpdateCoordinator,
) -> None:
    """Test WattboxPowerSensor native_value property."""
    sensor = WattboxPowerSensor(
        coordinator=mock_coordinator,
        entry_id="test_entry_id",
    )

    # Test with data
    assert sensor.native_value == 144.6

    # Test without data
    mock_coordinator.data = {}
    assert sensor.native_value is None


def test_sensor_inheritance(
    mock_coordinator: DataUpdateCoordinator,
) -> None:
    """Test that sensors inherit from correct base classes."""
    voltage_sensor = WattboxVoltageSensor(
        coordinator=mock_coordinator,
        entry_id="test_entry_id",
    )
    
    current_sensor = WattboxCurrentSensor(
        coordinator=mock_coordinator,
        entry_id="test_entry_id",
    )
    
    power_sensor = WattboxPowerSensor(
        coordinator=mock_coordinator,
        entry_id="test_entry_id",
    )

    assert isinstance(voltage_sensor, SensorEntity)
    assert isinstance(current_sensor, SensorEntity)
    assert isinstance(power_sensor, SensorEntity)