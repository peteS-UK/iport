import logging

from typing import Any, Dict, Optional

import voluptuous as vol

from .const import DOMAIN, CONF_AREA

from homeassistant import config_entries, core,  exceptions
from homeassistant.const import CONF_HOST, CONF_NAME
from homeassistant.core import callback
from homeassistant.helpers.aiohttp_client import async_get_clientsession
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity_registry import (
    async_entries_for_config_entry,
    async_get,
)


_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = vol.Schema(
    {vol.Required(CONF_HOST): cv.string, 
    vol.Optional(CONF_NAME): cv.string,
    vol.Optional("area_1", default="Area 1"): cv.string,
    vol.Optional("area_2", default="Area 2"): cv.string,
    vol.Optional("area_3", default="Area 3"): cv.string,
    vol.Optional("area_4", default="Area 4"): cv.string,
    vol.Optional("area_5", default="Area 5"): cv.string,
    vol.Optional("area_6", default="Area 6"): cv.string,
    vol.Optional("area_7", default="Area 7"): cv.string,
    vol.Optional("area_8", default="Area 8"): cv.string
    }
)

class SelectError(exceptions.HomeAssistantError):
    """Error"""
    pass


async def validate_auth(hass: core.HomeAssistant, data: dict) -> None:

    if "host" not in data.keys():
        data["host"] = ""
    if "name" not in data.keys():
        data["name"] = ""


    if ( (len(data["host"]) <3 or len(data["name"])<1)):
        # Manual entry requires host and name
        raise ValueError

class IPORTConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):

    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    async def async_step_user(self, user_input = None):
        """Invoked when a user initiates a flow via the user interface."""
        errors: Dict[str, str] = {}
        if user_input is not None:
            try:
                await validate_auth(self.hass, user_input)
            except ValueError:
                errors["base"] = "data"
            except SelectError:
                errors["base"] = "select"
            if not errors:
                # Input is valid, set data.
                self.data = user_input
                return self.async_create_entry(title="Light Symphony iPort", data=self.data)

        # If there is no user input or there were errors, show the form again, including any errors that were found with the input.
        return self.async_show_form(
            step_id="user", data_schema=CONFIG_SCHEMA, errors=errors
        )

