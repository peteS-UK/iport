"""Config flow for iPort integration."""

import homeassistant.helpers.config_validation as cv
import probatio
from homeassistant import config_entries, core, exceptions
from homeassistant.const import CONF_HOST, CONF_NAME

from .const import DOMAIN

CONFIG_SCHEMA = probatio.Schema(
    {
        probatio.Optional(CONF_HOST): cv.string,
        probatio.Required(CONF_NAME): cv.string,
        probatio.Required("area_count", default="8"): cv.string,
        probatio.Optional("area_1", default="Area 1"): cv.string,
        probatio.Optional("area_2", default="Area 2"): cv.string,
        probatio.Optional("area_3", default="Area 3"): cv.string,
        probatio.Optional("area_4", default="Area 4"): cv.string,
        probatio.Optional("area_5", default="Area 5"): cv.string,
        probatio.Optional("area_6", default="Area 6"): cv.string,
        probatio.Optional("area_7", default="Area 7"): cv.string,
        probatio.Optional("area_8", default="Area 8"): cv.string,
        probatio.Optional("area_9", default="Area 9"): cv.string,
        probatio.Optional("area_10", default="Area 10"): cv.string,
        probatio.Optional("area_11", default="Area 11"): cv.string,
        probatio.Optional("area_12", default="Area 12"): cv.string,
        probatio.Optional("area_13", default="Area 13"): cv.string,
        probatio.Optional("area_14", default="Area 14"): cv.string,
        probatio.Optional("area_15", default="Area 15"): cv.string,
    }
)


MAX_AREAS = 15


def _options_schema(current: dict) -> probatio.Schema:
    """Build the options schema using the current values as defaults."""
    schema = {
        probatio.Required(
            "area_count", default=str(current.get("area_count", "8"))
        ): cv.string
    }
    for i in range(1, MAX_AREAS + 1):
        key = f"area_{i}"
        schema[probatio.Optional(key, default=current.get(key, f"Area {i}"))] = (
            cv.string
        )
    return probatio.Schema(schema)


class IPORTOptionsFlow(config_entries.OptionsFlow):
    """Options flow to change the area count and area names."""

    async def async_step_init(self, user_input=None):
        errors: dict[str, str] = {}
        if user_input is not None:
            try:
                count = int(user_input["area_count"])
                if not 1 <= count <= MAX_AREAS:
                    raise ValueError
            except ValueError:
                errors["base"] = "area_count"
            if not errors:
                return self.async_create_entry(title="", data=user_input)

        current = {**self.config_entry.data, **self.config_entry.options}
        return self.async_show_form(
            step_id="init", data_schema=_options_schema(current), errors=errors
        )


class SelectError(exceptions.HomeAssistantError):
    """Error"""

    pass


async def validate_auth(hass: core.HomeAssistant, data: dict) -> None:
    if "name" not in data:
        data["name"] = ""

    if len(data["name"]) < 1:
        # Manual entry requires host and name
        raise ValueError


@config_entries.HANDLERS.register(DOMAIN)
class IPORTConfigFlow(config_entries.ConfigFlow):
    @staticmethod
    @core.callback
    def async_get_options_flow(config_entry):
        return IPORTOptionsFlow()

    async def async_step_user(self, user_input=None):
        """Invoked when a user initiates a flow via the user interface."""
        errors: dict[str, str] = {}
        if user_input is not None:
            try:
                await validate_auth(self.hass, user_input)
            except ValueError:
                errors["base"] = "data"
            except SelectError:
                errors["base"] = "select"
            if not errors:
                # Host if given, otherwise the device name (host is optional)
                await self.async_set_unique_id(
                    user_input.get(CONF_HOST) or user_input[CONF_NAME]
                )
                self._abort_if_unique_id_configured()
                # Input is valid, set data.
                self.data = user_input
                return self.async_create_entry(
                    title="Light Symphony iPort", data=self.data
                )

        # If there is no user input or there were errors, show the form again, including any errors that were found with the input.
        return self.async_show_form(
            step_id="user", data_schema=CONFIG_SCHEMA, errors=errors
        )
