"""The emotiva component."""

import logging

from homeassistant import config_entries, core
from homeassistant.const import Platform
from homeassistant.const import CONF_HOST, CONF_NAME

from .iport import IPORT

from .const import (
	DOMAIN,
	CONF_AREA,
	CONF_AREA_COUNT,
	DEFAULT_NAME
)

_LOGGER = logging.getLogger(__name__)

PLATFORMS = [Platform.SWITCH]


async def async_setup_entry(
	hass: core.HomeAssistant, entry: config_entries.ConfigEntry
) -> bool:
	"""Set up platform from a ConfigEntry."""
	hass.data.setdefault(DOMAIN, {})
	hass_data = dict(entry.data)


	iPortIP = hass_data.get(CONF_HOST,None)

	if iPortIP is None:
		_LOGGER.debug("No IP, so try discovery")
		iPortIP = await hass.async_add_executor_job(IPORT.discover)

	if iPortIP is None:
		_LOGGER.critical("No iPort IP specified, and discovery failed")
		return False
	
	_LOGGER.debug("iPortIP: %s", iPortIP)
	
	iport = IPORT(iPortIP,hass_data[CONF_NAME])

	await iport.async_udp_connect()

	for i in range(int(hass_data[CONF_AREA_COUNT])):
		iport._port_name.append(hass_data[CONF_AREA + str(i+1)])

	hass_data["iport"] = iport

	hass.data[DOMAIN][entry.entry_id] = hass_data

	await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

	return True


async def async_unload_entry(
	hass: core.HomeAssistant, entry: config_entries.ConfigEntry
) -> bool:
	"""Unload a config entry."""
	if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
		# Remove config entry from domain.
		iport = hass.data[DOMAIN][entry.entry_id]["iport"]
		await iport.async_udp_disconnect()
		entry_data = hass.data[DOMAIN].pop(entry.entry_id)


	return unload_ok

