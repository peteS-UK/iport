from __future__ import annotations

import logging

import voluptuous as vol
from homeassistant import config_entries, core
from homeassistant.components.switch import PLATFORM_SCHEMA, SwitchEntity
from homeassistant.const import CONF_HOST, CONF_NAME
from homeassistant.helpers import (
    config_validation as cv,
)
from homeassistant.helpers import (
    entity_platform,
)
from homeassistant.helpers.device_registry import DeviceInfo

from .const import (
    CONF_AREA,
    CONF_AREA_COUNT,
    DOMAIN,
    SERVICE_SEND_COMMAND,
)

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Optional(CONF_HOST): cv.string,
        vol.Required(CONF_NAME): cv.string,
        vol.Optional(CONF_AREA + "1", default="Area 1"): cv.string,
        vol.Optional(CONF_AREA + "2", default="Area 2"): cv.string,
        vol.Optional(CONF_AREA + "3", default="Area 3"): cv.string,
        vol.Optional(CONF_AREA + "4", default="Area 4"): cv.string,
        vol.Optional(CONF_AREA + "5", default="Area 5"): cv.string,
        vol.Optional(CONF_AREA + "6", default="Area 6"): cv.string,
        vol.Optional(CONF_AREA + "7", default="Area 7"): cv.string,
        vol.Optional(CONF_AREA + "8", default="Area 8"): cv.string,
        vol.Optional(CONF_AREA + "9", default="Area 9"): cv.string,
        vol.Optional(CONF_AREA + "10", default="Area 10"): cv.string,
        vol.Optional(CONF_AREA + "11", default="Area 11"): cv.string,
        vol.Optional(CONF_AREA + "12", default="Area 12"): cv.string,
        vol.Optional(CONF_AREA + "13", default="Area 13"): cv.string,
        vol.Optional(CONF_AREA + "14", default="Area 14"): cv.string,
        vol.Optional(CONF_AREA + "15", default="Area 15"): cv.string,
    }
)


async def async_setup_entry(
    hass: core.HomeAssistant,
    config_entry: config_entries.ConfigEntry,
    async_add_entities,
) -> None:
    config = hass.data[DOMAIN][config_entry.entry_id]

    iport = config["iport"]

    area_count = int(config[CONF_AREA_COUNT])
    areas = []

    for port in range(1, area_count + 1):
        areas.append(IPORTDevice(iport, iport._port_name[port - 1], port, hass))

    async_add_entities(areas)

    # Register entity services
    platform = entity_platform.async_get_current_platform()
    platform.async_register_entity_service(
        SERVICE_SEND_COMMAND,
        {
            vol.Required("Command"): cv.string,
            vol.Optional("Value"): cv.string,
        },
        IPORTDevice.send_command.__name__,
    )


class IPORTDevice(SwitchEntity):
    # Representation of a IPORT

    def __init__(self, device, port_name, port_number, hass):
        self._device = device
        self._port_name = port_name
        self._port_number = port_number
        self._hass = hass
        self._entity_id = "switch.iport_area_" + str(port_number)
        self._unique_id = "iport_area_" + str(port_number)

    @property
    def should_poll(self):
        return False

    @property
    def name(self):
        return self._port_name

    @property
    def has_entity_name(self):
        return True

    @property
    def device_info(self) -> DeviceInfo:
        """Return the device info."""
        return DeviceInfo(
            identifiers={
                # Serial numbers are unique identifiers within a specific domain
                (DOMAIN, self._device._name)
            },
            name=self._device._name,
            manufacturer="Light Symphony",
            model="iPort",
        )

    @property
    def unique_id(self):
        return self._unique_id

    @property
    def entity_id(self):
        return self._entity_id

    @entity_id.setter
    def entity_id(self, entity_id):
        self._entity_id = entity_id

    @property
    def is_on(self):
        return self._device.state

    async def async_turn_on(self, **kwargs):
        await self._device.async_turn_on(self._port_number)
        self._device.state = True
        self.async_schedule_update_ha_state(force_refresh=False)

    async def async_turn_off(self, **kwargs):
        await self._device.async_turn_off(self._port_number)
        self._device.state = False
        self.async_schedule_update_ha_state(force_refresh=False)

    async def send_command(self, Command, Value=None):
        _LOGGER.debug("Send Command %s for port %d", Command, self._port_number)
        await self._device.async_send_command(Command, self._port_number, Value)
        self.async_schedule_update_ha_state(force_refresh=False)
