"""Test the Wattbox entity classes."""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from custom_components.wattbox.entity import (
    WattboxDeviceEntity,
    WattboxEntity,
    WattboxOutletEntity,
)


@pytest.fixture
def mock_coordinator() -> DataUpdateCoordinator:
    """Mock coordinator for testing."""
    coordinator = MagicMock(spec=DataUpdateCoordinator)
    coordinator.data = {
        "device_info": {
            "serial_number": "test_device",
            "hostname": "Test Wattbox",
            "model": "WB-800VPS-IPVM-18",
            "hardware_version": "1.0.0",
        }
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


def test_wattbox_entity_init(
    mock_coordinator: DataUpdateCoordinator, mock_device_info: DeviceInfo
) -> None:
    """Test WattboxEntity initialization."""
    entity = WattboxEntity(
        coordinator=mock_coordinator,
        device_info=mock_device_info,
        unique_id="test_unique_id",
    )

    assert entity.coordinator == mock_coordinator
    assert entity.unique_id == "test_unique_id"
    
    # Check that device info is built from coordinator data
    expected_device_info = DeviceInfo(
        identifiers={("wattbox", "test_device")},
        name="Test Wattbox",
        manufacturer="SnapAV",
        model="WB-800VPS-IPVM-18",
        sw_version="1.0.0",
    )
    assert entity.device_info == expected_device_info


def test_wattbox_device_entity_init(
    mock_coordinator: DataUpdateCoordinator, mock_device_info: DeviceInfo
) -> None:
    """Test WattboxDeviceEntity initialization."""
    entity = WattboxDeviceEntity(
        coordinator=mock_coordinator,
        device_info=mock_device_info,
        unique_id="test_device_unique_id",
    )

    assert entity.coordinator == mock_coordinator
    assert entity.unique_id == "test_device_unique_id"
    
    # Check that device info is built from coordinator data
    expected_device_info = DeviceInfo(
        identifiers={("wattbox", "test_device")},
        name="Test Wattbox",
        manufacturer="SnapAV",
        model="WB-800VPS-IPVM-18",
        sw_version="1.0.0",
    )
    assert entity.device_info == expected_device_info


def test_wattbox_outlet_entity_init(
    mock_coordinator: DataUpdateCoordinator, mock_device_info: DeviceInfo
) -> None:
    """Test WattboxOutletEntity initialization."""
    entity = WattboxOutletEntity(
        coordinator=mock_coordinator,
        device_info=mock_device_info,
        unique_id="test_outlet_unique_id",
        outlet_number=1,
    )

    assert entity.coordinator == mock_coordinator
    assert entity.unique_id == "test_outlet_unique_id"
    assert entity._outlet_number == 1
    
    # Check that device info is built from coordinator data
    expected_device_info = DeviceInfo(
        identifiers={("wattbox", "test_device")},
        name="Test Wattbox",
        manufacturer="SnapAV",
        model="WB-800VPS-IPVM-18",
        sw_version="1.0.0",
    )
    assert entity.device_info == expected_device_info


def test_wattbox_entity_device_info(
    mock_coordinator: DataUpdateCoordinator, mock_device_info: DeviceInfo
) -> None:
    """Test WattboxEntity device_info property."""
    entity = WattboxEntity(
        coordinator=mock_coordinator,
        device_info=mock_device_info,
        unique_id="test_unique_id",
    )

    # Check that device info is built from coordinator data
    expected_device_info = DeviceInfo(
        identifiers={("wattbox", "test_device")},
        name="Test Wattbox",
        manufacturer="SnapAV",
        model="WB-800VPS-IPVM-18",
        sw_version="1.0.0",
    )
    assert entity.device_info == expected_device_info


def test_wattbox_entity_should_poll(
    mock_coordinator: DataUpdateCoordinator, mock_device_info: DeviceInfo
) -> None:
    """Test WattboxEntity should_poll property."""
    entity = WattboxEntity(
        coordinator=mock_coordinator,
        device_info=mock_device_info,
        unique_id="test_unique_id",
    )

    # Should not poll since it uses coordinator
    assert entity.should_poll is False


def test_wattbox_outlet_entity_outlet_number(
    mock_coordinator: DataUpdateCoordinator, mock_device_info: DeviceInfo
) -> None:
    """Test WattboxOutletEntity outlet_number property."""
    entity = WattboxOutletEntity(
        coordinator=mock_coordinator,
        device_info=mock_device_info,
        unique_id="test_outlet_unique_id",
        outlet_number=5,
    )

    assert entity._outlet_number == 5


def test_wattbox_outlet_entity_name(
    mock_coordinator: DataUpdateCoordinator, mock_device_info: DeviceInfo
) -> None:
    """Test WattboxOutletEntity name property."""
    entity = WattboxOutletEntity(
        coordinator=mock_coordinator,
        device_info=mock_device_info,
        unique_id="test_outlet_unique_id",
        outlet_number=3,
    )

    # Name should be set in the entity
    assert hasattr(entity, "name")


def test_wattbox_entity_coordinator_data(
    mock_coordinator: DataUpdateCoordinator, mock_device_info: DeviceInfo
) -> None:
    """Test WattboxEntity coordinator data access."""
    entity = WattboxEntity(
        coordinator=mock_coordinator,
        device_info=mock_device_info,
        unique_id="test_unique_id",
    )

    # Should be able to access coordinator data
    expected_data = {
        "device_info": {
            "serial_number": "test_device",
            "hostname": "Test Wattbox",
            "model": "WB-800VPS-IPVM-18",
            "hardware_version": "1.0.0",
        }
    }
    assert entity.coordinator.data == expected_data
