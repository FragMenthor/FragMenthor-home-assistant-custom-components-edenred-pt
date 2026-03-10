import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback

from .const import DOMAIN, CONF_EMAIL, CONF_PASSWORD, CONF_INTERVAL, MIN_INTERVAL, MAX_INTERVAL

class EdenredConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return EdenredOptionsFlow(config_entry)

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="Edenred Portugal", data=user_input)

        data_schema = vol.Schema({
            vol.Required(CONF_EMAIL): str,
            vol.Required(CONF_PASSWORD): str,
            vol.Required(CONF_INTERVAL, default=60): vol.All(vol.Coerce(int), vol.Range(min=MIN_INTERVAL, max=MAX_INTERVAL))
        })

        return self.async_show_form(step_id="user", data_schema=data_schema)

class EdenredOptionsFlow(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="Opções", data={CONF_INTERVAL: user_input[CONF_INTERVAL]})

        current = self.config_entry.options.get(CONF_INTERVAL, self.config_entry.data.get(CONF_INTERVAL, 60))

        data_schema = vol.Schema({
            vol.Required(CONF_INTERVAL, default=current): vol.All(vol.Coerce(int), vol.Range(min=MIN_INTERVAL, max=MAX_INTERVAL))
        })

        return self.async_show_form(step_id="init", data_schema=data_schema)
