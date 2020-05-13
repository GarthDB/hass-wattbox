"""Switch platform for blueprint."""
import logging

from homeassistant.components.switch import SwitchDevice
from homeassistant.const import CONF_NAME

from . import WattBoxEntity
from .const import DOMAIN_DATA, PLUG_ICON

_LOGGER = logging.getLogger(__name__)


async def async_setup_platform(
    hass, config, async_add_entities, discovery_info=None
):  # pylint: disable=unused-argument
    """Setup switch platform."""
    name = discovery_info[CONF_NAME]
    entities = []

    num_switches = hass.data[DOMAIN_DATA][name].number_outlets

    entities.append(WattBoxMasterSwitch(hass, name))
    for i in range(1, num_switches + 1):
        entities.append(WattBoxBinarySwitch(hass, name, i))

    async_add_entities(entities, True)


class WattBoxBinarySwitch(WattBoxEntity, SwitchDevice):
    """WattBox switch class."""

    def __init__(self, hass, name, index):
        super().__init__(hass, name, index)
        self.index = index
        self._status = False
        self._name = name + " Outlet " + str(index)

    async def async_update(self):
        """Update the sensor."""
        # Get new data (if any)
        outlet = self.hass.data[DOMAIN_DATA][self.wattbox_name].outlets[self.index]

        # Check the data and update the value.
        self._status = outlet.status

        # Set/update attributes
        self.attr["name"] = outlet.name
        self.attr["method"] = outlet.method
        self.attr["index"] = outlet.index

    async def async_turn_on(self, **kwargs):  # pylint: disable=unused-argument
        """Turn on the switch."""
        _LOGGER.debug(
            "Turning On: %s - %s",
            self.hass.data[DOMAIN_DATA][self.wattbox_name],
            self.hass.data[DOMAIN_DATA][self.wattbox_name].outlets[self.index],
        )
        _LOGGER.debug(
            "Current Outlet Before: %s - %s",
            self.hass.data[DOMAIN_DATA][self.wattbox_name].outlets[self.index].status,
            repr(self.hass.data[DOMAIN_DATA][self.wattbox_name].outlets[self.index]),
        )
        await self.hass.async_add_executor_job(
            self.hass.data[DOMAIN_DATA][self.wattbox_name].outlets[self.index].turn_on
        )
        await self.async_update()
        _LOGGER.debug(
            "Current Outlet After: %s - %s",
            self.hass.data[DOMAIN_DATA][self.wattbox_name].outlets[self.index].status,
            repr(self.hass.data[DOMAIN_DATA][self.wattbox_name].outlets[self.index]),
        )

    async def async_turn_off(self, **kwargs):  # pylint: disable=unused-argument
        """Turn off the switch."""
        _LOGGER.debug(
            "Turning Off: %s - %s",
            self.hass.data[DOMAIN_DATA][self.wattbox_name],
            self.hass.data[DOMAIN_DATA][self.wattbox_name].outlets[self.index],
        )
        _LOGGER.debug(
            "Current Outlet Before: %s - %s",
            self.hass.data[DOMAIN_DATA][self.wattbox_name].outlets[self.index].status,
            repr(self.hass.data[DOMAIN_DATA][self.wattbox_name].outlets[self.index]),
        )
        await self.hass.async_add_executor_job(
            self.hass.data[DOMAIN_DATA][self.wattbox_name].outlets[self.index].turn_off
        )
        await self.async_update()
        _LOGGER.debug(
            "Current Outlet After: %s - %s",
            self.hass.data[DOMAIN_DATA][self.wattbox_name].outlets[self.index].status,
            repr(self.hass.data[DOMAIN_DATA][self.wattbox_name].outlets[self.index]),
        )

    @property
    def icon(self):
        """Return the icon of this switch."""
        return PLUG_ICON

    @property
    def is_on(self):
        """Return true if the switch is on."""
        return self._status


class WattBoxMasterSwitch(WattBoxBinarySwitch):
    def __init__(self, hass, name):
        self.hass = hass
        self.attr = {}
        self.index = 0
        self.wattbox_name = name
        self._status = False
        self._name = name + " Master Switch"
