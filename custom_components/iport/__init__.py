"""The Light Symphony iport component."""

import logging

from homeassistant import config_entries, core
from homeassistant.const import CONF_HOST, CONF_NAME, Platform
from homeassistant.exceptions import ConfigEntryNotReady

from .iport import IPORT

_LOGGER = logging.getLogger(__name__)

PLATFORMS = [Platform.SWITCH]

type IPortConfigEntry = config_entries.ConfigEntry[IPORT]


async def async_setup_entry(hass: core.HomeAssistant, entry: IPortConfigEntry) -> bool:
    """Set up platform from a ConfigEntry."""
    hass_data = {**entry.data, **entry.options}

    iPortIP = hass_data.get(CONF_HOST, None)

    if not iPortIP:
        _LOGGER.debug("No IP, so try discovery")
        iPortIP = await hass.async_add_executor_job(IPORT.discover)

    if not iPortIP:
        raise ConfigEntryNotReady("No iPort IP specified, and discovery failed")

    _LOGGER.debug("iPortIP: %s", iPortIP)

    iport = IPORT(iPortIP, hass_data[CONF_NAME])

    try:
        await iport.async_udp_connect()
    except Exception as err:
        raise ConfigEntryNotReady(f"Cannot connect to iPort at {iPortIP}") from err

    entry.runtime_data = iport

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    entry.async_on_unload(entry.add_update_listener(_async_update_listener))

    return True


async def _async_update_listener(
    hass: core.HomeAssistant, entry: config_entries.ConfigEntry
) -> None:
    """Reload the entry when options change."""
    await hass.config_entries.async_reload(entry.entry_id)


async def async_unload_entry(hass: core.HomeAssistant, entry: IPortConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        await entry.runtime_data.async_udp_disconnect()

    return unload_ok
