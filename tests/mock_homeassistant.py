"""Mock Home Assistant modules for CI testing."""

from __future__ import annotations

from enum import Enum
from typing import Any, Dict, Optional
from unittest.mock import AsyncMock, MagicMock


class FlowResultType(Enum):
    """Mock FlowResultType enum."""
    FORM = "form"
    CREATE_ENTRY = "create_entry"
    ABORT = "abort"
    EXTERNAL_STEP = "external_step"
    EXTERNAL_STEP_DONE = "external_step_done"
    SHOW_PROGRESS = "show_progress"
    SHOW_PROGRESS_DONE = "show_progress_done"
    MENU = "menu"


class HomeAssistant:
    """Mock HomeAssistant class."""
    
    def __init__(self, config_dir: str):
        self.config_dir = config_dir
        self.data: Dict[str, Any] = {}
        self.config_entries = MagicMock()
        self.entity_registry = MagicMock()
        self.device_registry = MagicMock()
    
    async def async_start(self):
        """Mock async_start."""
        pass
    
    async def async_stop(self):
        """Mock async_stop."""
        pass


class ConfigEntry:
    """Mock ConfigEntry class."""
    
    def __init__(self, **kwargs):
        self.entry_id = kwargs.get("entry_id", "test_entry_id")
        self.data = kwargs.get("data", {})
        self.options = kwargs.get("options", {})
        self.title = kwargs.get("title", "Test Entry")
        self.domain = kwargs.get("domain", "wattbox")
        self.source = kwargs.get("source", "user")
        self.version = kwargs.get("version", 1)
        self.minor_version = kwargs.get("minor_version", 1)
        self.state = kwargs.get("state", "loaded")
        self.pref_disable_new_entities = kwargs.get("pref_disable_new_entities", False)
        self.pref_disable_polling = kwargs.get("pref_disable_polling", False)
        self.disabled_by = kwargs.get("disabled_by", None)
        self.reason = kwargs.get("reason", None)


class DeviceInfo:
    """Mock DeviceInfo class."""
    
    def __init__(self, **kwargs):
        self.identifiers = kwargs.get("identifiers", set())
        self.connections = kwargs.get("connections", set())
        self.manufacturer = kwargs.get("manufacturer", "")
        self.model = kwargs.get("model", "")
        self.name = kwargs.get("name", "")
        self.suggested_area = kwargs.get("suggested_area", "")
        self.sw_version = kwargs.get("sw_version", "")
        self.hw_version = kwargs.get("hw_version", "")
        self.serial_number = kwargs.get("serial_number", "")
        self.configuration_url = kwargs.get("configuration_url", "")


class DataUpdateCoordinator:
    """Mock DataUpdateCoordinator class."""
    
    def __init__(self, hass: HomeAssistant, **kwargs):
        self.hass = hass
        self.data = {}
        self.last_update_success = True
        self.last_update_time = None
        self.update_interval = kwargs.get("update_interval", 30)
    
    async def async_config_entry_first_refresh(self):
        """Mock async_config_entry_first_refresh."""
        pass
    
    async def async_request_refresh(self):
        """Mock async_request_refresh."""
        pass


class UpdateFailed(Exception):
    """Mock UpdateFailed exception."""
    pass


class BinarySensorEntity:
    """Mock BinarySensorEntity class."""
    pass


class SensorEntity:
    """Mock SensorEntity class."""
    pass


class SwitchEntity:
    """Mock SwitchEntity class."""
    pass


# Create mock modules
class MockModule:
    """Mock module class."""
    
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


# Mock the homeassistant module structure
homeassistant = MockModule(
    core=MockModule(HomeAssistant=HomeAssistant),
    config_entries=MockModule(ConfigEntry=ConfigEntry),
    data_entry_flow=MockModule(FlowResultType=FlowResultType),
    helpers=MockModule(
        entity=MockModule(DeviceInfo=DeviceInfo),
        update_coordinator=MockModule(
            DataUpdateCoordinator=DataUpdateCoordinator,
            UpdateFailed=UpdateFailed
        )
    ),
    components=MockModule(
        binary_sensor=MockModule(BinarySensorEntity=BinarySensorEntity),
        sensor=MockModule(SensorEntity=SensorEntity),
        switch=MockModule(SwitchEntity=SwitchEntity)
    )
)
