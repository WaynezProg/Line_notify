from homeassistant import config_entries
from typing import Any, Dict, Optional
from .const import DOMAIN
from homeassistant.const import CONF_ACCESS_TOKEN,CONF_NAME
import voluptuous as vol

# PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
#     vol.Required(CONF_ACCESS_TOKEN): cv.string,
# })

class lineNotifyFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    def __init__(self):
        """Initialize an instance of the squeezebox config flow."""
        self.discovery_info = None

    async def async_step_user(self, user_input= None):
        errors = {}
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")
        if user_input is not None:
            errors = await self._check_input(user_input)
            if not errors:
                return self.async_create_entry(title=user_input[CONF_NAME], data=user_input)

        else:
            user_input = {}

        return self.async_show_form(
            step_id="user",
            data_schema = vol.Schema({
                    vol.Required(CONF_NAME, default=user_input.get(CONF_NAME, vol.UNDEFINED)): str,
                    vol.Required(CONF_ACCESS_TOKEN, default=user_input.get(CONF_ACCESS_TOKEN,vol.UNDEFINED)): str,
                }),
            errors=errors,

        )

    def async_get_options_flow(entry: config_entries.ConfigEntry):
        return OptionsFlowHandler(entry)
    async def _check_input(self, config):
        errors = {}
        token = config.get(CONF_ACCESS_TOKEN)
        if self._async_host_already_configured(token):
            errors["base"] = "already_configured"
        return errors


    def _async_host_already_configured(self, token):
        """See if we already have an entry matching the host."""
        for entry in self._async_current_entries():
            if entry.data.get(CONF_ACCESS_TOKEN) == token:
                return True
        return False

class OptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, entry: config_entries.ConfigEntry):
        self.entry = entry

    async def async_step_init(self, user_input=None):
        errors = {}
        if user_input is not None:
            return self.async_create_entry(title=user_input[CONF_NAME], data=user_input)

        else:
            user_input = {}
        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Required(CONF_NAME, default=self.entry.options.get(CONF_NAME, self.entry.data.get(CONF_NAME))): str,
                vol.Required(CONF_ACCESS_TOKEN, default=self.entry.options.get(CONF_ACCESS_TOKEN, self.entry.data.get(CONF_ACCESS_TOKEN))): str,
            }),
            errors=errors,
        )
