"""Mock Home Assistant modules for CI testing."""

from __future__ import annotations

from enum import Enum
from typing import Any, Dict
from unittest.mock import MagicMock


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


class FlowResult:
    """Mock FlowResult class."""

    def __init__(self, flow_id: str, type: FlowResultType, data: dict = None):
        self.flow_id = flow_id
        self.type = type
        self.data = data or {}

    def __getitem__(self, key):
        """Make FlowResult subscriptable like a dictionary."""
        if key == "type":
            return self.type
        elif key == "data":
            # For CREATE_ENTRY type, return just the data dict without title
            if self.type == FlowResultType.CREATE_ENTRY:
                data_without_title = self.data.copy()
                data_without_title.pop("title", None)
                return data_without_title
            # For other types, return the full data structure
            return self.data
        elif key == "flow_id":
            return self.flow_id
        elif key == "step_id":
            return self.data.get("step_id")
        elif key == "errors":
            return self.data.get("errors", {})
        elif key == "title":
            return self.data.get("title")
        else:
            # For any other key, try to get it from data
            return self.data.get(key)

    def __contains__(self, key):
        """Support 'key in result' checks."""
        if key == "type" or key == "data" or key == "flow_id":
            return True
        return key in self.data


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
        self.disabled_by = kwargs.get("disabled_by")
        self.reason = kwargs.get("reason")


class ConfigFlow:
    """Mock ConfigFlow class."""

    def __init__(self, *args, **kwargs):
        pass

    def __init_subclass__(cls, domain=None, **kwargs):
        """Mock __init_subclass__ to handle domain parameter."""
        cls.domain = domain
        super().__init_subclass__(**kwargs)

    def async_show_form(self, step_id, data_schema=None, errors=None):
        """Mock async_show_form method."""
        data = {"step_id": step_id}
        if errors:
            data["errors"] = errors
        return FlowResult("test_flow", FlowResultType.FORM, data)

    def async_create_entry(self, title, data):
        """Mock async_create_entry method."""
        # Include title in the data for CREATE_ENTRY
        data_with_title = data.copy()
        data_with_title["title"] = title
        return FlowResult("test_flow", FlowResultType.CREATE_ENTRY, data_with_title)

    def async_abort(self, reason):
        """Mock async_abort method."""
        return FlowResult("test_flow", FlowResultType.ABORT, {"reason": reason})


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

    def __eq__(self, other):
        """Compare DeviceInfo objects for equality."""
        if not isinstance(other, DeviceInfo):
            return False
        return (
            self.identifiers == other.identifiers
            and self.connections == other.connections
            and self.manufacturer == other.manufacturer
            and self.model == other.model
            and self.name == other.name
            and self.suggested_area == other.suggested_area
            and self.sw_version == other.sw_version
            and self.hw_version == other.hw_version
            and self.serial_number == other.serial_number
            and self.configuration_url == other.configuration_url
        )


class DataUpdateCoordinator:
    """Mock DataUpdateCoordinator class."""

    def __init__(self, hass: HomeAssistant, logger=None, **kwargs):
        self.hass = hass
        self.logger = logger
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

    def __class_getitem__(self, item):
        """Support generic type parameters like DataUpdateCoordinator[dict[str, Any]]."""
        return self


class UpdateFailed(Exception):
    """Mock UpdateFailed exception."""

    pass


class HomeAssistantError(Exception):
    """Mock HomeAssistantError exception."""

    pass


class BinarySensorEntity:
    """Mock BinarySensorEntity class."""

    pass


class SensorEntity:
    """Mock SensorEntity class."""

    def __init__(self):
        self._attr_native_unit_of_measurement = None

    @property
    def native_unit_of_measurement(self):
        """Mock native_unit_of_measurement property."""
        return self._attr_native_unit_of_measurement


class SwitchEntity:
    """Mock SwitchEntity class."""

    pass


# Create mock modules
class MockModule:
    """Mock module class."""

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


# Mock constants
class Platform:
    """Mock Platform enum."""

    BINARY_SENSOR = "binary_sensor"
    SENSOR = "sensor"
    SWITCH = "switch"


class UnitOfElectricPotential:
    """Mock UnitOfElectricPotential enum."""

    VOLT = "V"


class UnitOfPower:
    """Mock UnitOfPower enum."""

    WATT = "W"


# Mock configuration constants
CONF_HOST = "host"
CONF_PASSWORD = "password"
CONF_USERNAME = "username"


class MockFrame:
    """Mock frame module."""

    def report_usage(self, *args, **kwargs):
        """Mock report_usage function."""
        pass


class AddEntitiesCallback:
    """Mock AddEntitiesCallback type."""

    pass


class CoordinatorEntity:
    """Mock CoordinatorEntity class."""

    def __init__(self, coordinator):
        """Mock __init__ method that accepts coordinator parameter."""
        self.coordinator = coordinator
        self._attr_unique_id = None
        self._attr_name = None
        self._attr_device_class = None

    @property
    def unique_id(self):
        """Mock unique_id property."""
        return self._attr_unique_id

    @property
    def name(self):
        """Mock name property."""
        return self._attr_name

    @property
    def device_class(self):
        """Mock device_class property."""
        return self._attr_device_class


class MockVoluptuous:
    """Mock voluptuous module."""

    def __getattr__(self, name):
        """Mock any voluptuous attribute."""
        return lambda *args, **kwargs: None


# Mock the homeassistant module structure
homeassistant = MockModule(
    core=MockModule(HomeAssistant=HomeAssistant),
    config_entries=MockModule(ConfigEntry=ConfigEntry, ConfigFlow=ConfigFlow),
    data_entry_flow=MockModule(FlowResultType=FlowResultType, FlowResult=FlowResult),
    exceptions=MockModule(HomeAssistantError=HomeAssistantError),
    const=MockModule(
        Platform=Platform,
        UnitOfElectricPotential=UnitOfElectricPotential,
        UnitOfPower=UnitOfPower,
        CONF_HOST=CONF_HOST,
        CONF_PASSWORD=CONF_PASSWORD,
        CONF_USERNAME=CONF_USERNAME,
    ),
    helpers=MockModule(
        entity=MockModule(DeviceInfo=DeviceInfo),
        update_coordinator=MockModule(
            DataUpdateCoordinator=DataUpdateCoordinator,
            UpdateFailed=UpdateFailed,
            CoordinatorEntity=CoordinatorEntity,
        ),
        frame=MockFrame(),
        entity_platform=MockModule(AddEntitiesCallback=AddEntitiesCallback),
    ),
    components=MockModule(
        binary_sensor=MockModule(BinarySensorEntity=BinarySensorEntity),
        sensor=MockModule(SensorEntity=SensorEntity),
        switch=MockModule(SwitchEntity=SwitchEntity),
    ),
)

# Mock external dependencies
voluptuous = MockVoluptuous()
