from __future__ import annotations

import logging

import probatio
from homeassistant import config_entries, core
from homeassistant.components.switch import SwitchEntity
from homeassistant.helpers import (
    config_validation as cv,
)
from homeassistant.helpers import (
    entity_platform,
)
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.restore_state import RestoreEntity

from .const import (
    CONF_AREA,
    CONF_AREA_COUNT,
    DOMAIN,
    SERVICE_SEND_COMMAND,
)

_LOGGER = logging.getLogger(__name__)

PARALLEL_UPDATES = 1


async def async_setup_entry(
    hass: core.HomeAssistant,
    config_entry: config_entries.ConfigEntry,
    async_add_entities,
) -> None:
    iport = config_entry.runtime_data

    config = {**config_entry.data, **config_entry.options}
    area_count = int(config[CONF_AREA_COUNT])
    areas = []

    for port in range(1, area_count + 1):
        port_name = config.get(f"{CONF_AREA}{port}", f"Area {port}")
        areas.append(IPORTDevice(iport, port_name, port, hass))

    async_add_entities(areas)

    # Register entity services
    platform = entity_platform.async_get_current_platform()
    platform.async_register_entity_service(
        SERVICE_SEND_COMMAND,
        {
            probatio.Required("command"): cv.string,
            probatio.Optional("value"): cv.string,
        },
        IPORTDevice.send_command.__name__,
    )


class IPORTDevice(SwitchEntity, RestoreEntity):
    # Representation of a IPORT

    def __init__(self, device, port_name, port_number, hass):
        self._device = device
        self._port_name = port_name
        self._port_number = port_number
        self._hass = hass
        self._attr_assumed_state = True
        self._attr_is_on = False
        self._attr_should_poll = False
        self._attr_available = True
        self._attr_device_info = DeviceInfo(
            identifiers={
                # Serial numbers are unique identifiers within a specific domain
                (DOMAIN, self._device._name)
            },
            name=self._device._name,
            manufacturer="Light Symphony",
            model="iPort",
        )
        self._attr_unique_id = f"iport_area_{port_number}"
        self._attr_name = port_name
        self._attr_has_entity_name = True

    async def async_added_to_hass(self):
        """Restore last state on startup."""
        await super().async_added_to_hass()
        last_state = await self.async_get_last_state()

        if last_state:
            self._attr_is_on = last_state.state == "on"

    async def async_turn_on(self, **kwargs):
        await self._device.async_turn_on(self._port_number)
        self._attr_is_on = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        await self._device.async_turn_off(self._port_number)
        self._attr_is_on = False
        self.async_write_ha_state()

    async def send_command(self, command, value=None):
        _LOGGER.debug("Send Command %s for port %d", command, self._port_number)
        await self._device.async_send_command(command, self._port_number, value)
        self.async_write_ha_state()
