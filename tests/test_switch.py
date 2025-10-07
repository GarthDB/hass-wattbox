"""Test the Wattbox switch platform."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from custom_components.wattbox.switch import (
    async_setup_entry,
    WattboxSwitch,
)


@pytest.fixture
def mock_coordinator() -> DataUpdateCoordinator:
    """Mock coordinator for testing."""
    coordinator = MagicMock(spec=DataUpdateCoordinator)
    coordinator.data = {
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
    """Test async_setup_entry for switch platform."""
    # Mock the coordinator and device info
    with patch("custom_components.wattbox.switch.async_setup_entry") as mock_setup:
        mock_setup.return_value = True
        
        result = await async_setup_entry(hass, mock_config_entry)
        
        # Since this is a placeholder, it should return True
        assert result is True


def test_wattbox_switch_init(
    mock_coordinator: DataUpdateCoordinator, 
    mock_device_info: DeviceInfo
) -> None:
    """Test WattboxSwitch initialization."""
    switch = WattboxSwitch(
        coordinator=mock_coordinator,
        device_info=mock_device_info,
        unique_id="test_outlet_switch_1",
        outlet_number=1,
    )
    
    assert switch.coordinator == mock_coordinator
    assert switch.device_info == mock_device_info
    assert switch.unique_id == "test_outlet_switch_1"
    assert switch._outlet_number == 1


def test_wattbox_switch_name(
    mock_coordinator: DataUpdateCoordinator, 
    mock_device_info: DeviceInfo
) -> None:
    """Test WattboxSwitch name property."""
    switch = WattboxSwitch(
        coordinator=mock_coordinator,
        device_info=mock_device_info,
        unique_id="test_outlet_switch_1",
        outlet_number=1,
    )
    
    assert switch.name == "Outlet 1"


def test_wattbox_switch_is_on(
    mock_coordinator: DataUpdateCoordinator, 
    mock_device_info: DeviceInfo
) -> None:
    """Test WattboxSwitch is_on property."""
    switch = WattboxSwitch(
        coordinator=mock_coordinator,
        device_info=mock_device_info,
        unique_id="test_outlet_switch_1",
        outlet_number=1,
    )
    
    # Currently returns None (TODO implementation)
    assert switch.is_on is None


@pytest.mark.asyncio
async def test_wattbox_switch_async_turn_on(
    mock_coordinator: DataUpdateCoordinator, 
    mock_device_info: DeviceInfo
) -> None:
    """Test WattboxSwitch async_turn_on method."""
    switch = WattboxSwitch(
        coordinator=mock_coordinator,
        device_info=mock_device_info,
        unique_id="test_outlet_switch_1",
        outlet_number=1,
    )
    
    # Test turning on (currently just passes)
    await switch.async_turn_on()


@pytest.mark.asyncio
async def test_wattbox_switch_async_turn_off(
    mock_coordinator: DataUpdateCoordinator, 
    mock_device_info: DeviceInfo
) -> None:
    """Test WattboxSwitch async_turn_off method."""
    switch = WattboxSwitch(
        coordinator=mock_coordinator,
        device_info=mock_device_info,
        unique_id="test_outlet_switch_1",
        outlet_number=1,
    )
    
    # Test turning off (currently just passes)
    await switch.async_turn_off()


def test_wattbox_switch_outlet_number(
    mock_coordinator: DataUpdateCoordinator, 
    mock_device_info: DeviceInfo
) -> None:
    """Test WattboxSwitch outlet_number property."""
    switch = WattboxSwitch(
        coordinator=mock_coordinator,
        device_info=mock_device_info,
        unique_id="test_outlet_switch_5",
        outlet_number=5,
    )
    
    assert switch._outlet_number == 5


def test_switch_inheritance(mock_coordinator: DataUpdateCoordinator, mock_device_info: DeviceInfo) -> None:
    """Test that switches inherit from correct base classes."""
    switch = WattboxSwitch(
        coordinator=mock_coordinator,
        device_info=mock_device_info,
        unique_id="test_outlet_switch_1",
        outlet_number=1,
    )
    
    assert isinstance(switch, SwitchEntity)


def test_wattbox_switch_different_outlets(
    mock_coordinator: DataUpdateCoordinator, 
    mock_device_info: DeviceInfo
) -> None:
    """Test WattboxSwitch with different outlet numbers."""
    # Test outlet 1
    switch1 = WattboxSwitch(
        coordinator=mock_coordinator,
        device_info=mock_device_info,
        unique_id="test_outlet_switch_1",
        outlet_number=1,
    )
    
    # Test outlet 2
    switch2 = WattboxSwitch(
        coordinator=mock_coordinator,
        device_info=mock_device_info,
        unique_id="test_outlet_switch_2",
        outlet_number=2,
    )
    
    assert switch1._outlet_number == 1
    assert switch2._outlet_number == 2
    assert switch1.unique_id != switch2.unique_id
