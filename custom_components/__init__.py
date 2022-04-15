"""Support for Hangouts."""
import logging
import aiohttp
import time
import voluptuous as vol
from homeassistant import core

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EVENT_HOMEASSISTANT_STOP,CONF_ACCESS_TOKEN,CONF_NAME
from homeassistant.core import HomeAssistant

import homeassistant.helpers.config_validation as cv


from .const import (
    DOMAIN,
    IMAGEFILE,
    BASE_URL,
    ATTR_MESSAGE,
    ATTR_DATA,
    SERVICE_SEND_MESSAGE,
    MESSAGE_SCHEMA
)
from aiohttp.hdrs import AUTHORIZATION
_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Required(CONF_NAME): cv.string,
                vol.Required(CONF_ACCESS_TOKEN): cv.string
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)

async def async_setup_entry(hass: core.HomeAssistant, entry: ConfigEntry):
    hass.data[DOMAIN] = {
        CONF_NAME: entry.options.get(CONF_NAME, entry.data.get(CONF_NAME)),
        CONF_ACCESS_TOKEN: entry.options.get(CONF_ACCESS_TOKEN, entry.data.get(CONF_ACCESS_TOKEN))
    }
    async def async_handle_send_message(call):
        message = call.data.get(ATTR_MESSAGE)
        image = call.data.get("image") if call.data is not None and "image" in call.data else False
        img = "/var/lib/homex/hass-config/www/image/snap.jpg"
        payload = {'message': message}
        payload[IMAGEFILE] = open(str(img), 'rb') if image else None
        headers = {AUTHORIZATION: "Bearer " + hass.data[DOMAIN].get(CONF_ACCESS_TOKEN)}
        _LOGGER.debug(payload)
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
            for i in range(10):
                async with session.post(BASE_URL, data=payload, headers=headers) as resp:
                    data = await resp.text()
                    _LOGGER.debug(data)
                    if resp.status == 200:
                        status = True
                        break
                    else:
                        _LOGGER.error(resp.status)
                        time.sleep(3)
                        data = None
                        status = False
    hass.services.async_register(DOMAIN, SERVICE_SEND_MESSAGE, async_handle_send_message, MESSAGE_SCHEMA)
    return True
async def async_unload_entry(hass: core.HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    hass.data[DOMAIN].pop(entry.entry_id, None)

    return True
async def async_update_options(hass: core.HomeAssistant, entry: ConfigEntry):
    await hass.config_entries.async_reload(entry.entry_id)