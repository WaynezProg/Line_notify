import voluptuous as vol
from homeassistant.components.notify import ATTR_DATA, ATTR_MESSAGE
import homeassistant.helpers.config_validation as cv
DOMAIN = "line_notify"
SERVICE_SEND_MESSAGE = "send_message"
BASE_URL = 'https://notify-api.line.me/api/notify'
IMAGEFILE = 'imageFile'


MESSAGE_SCHEMA = vol.Schema(
    {
        vol.Required(ATTR_MESSAGE): cv.string,
        vol.Optional("image"): cv.boolean,
    }
)
