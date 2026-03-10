import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback

from .const import DOMAIN, CONF_EMAIL, CONF_PASSWORD, CONF_INTERVAL, MIN_INTERVAL, MAX_INTERVAL


def _sanitize_interval(value, default=60):
    try:
        iv = int(value)
    except (TypeError, ValueError):
        iv = default
    if iv < MIN_INTERVAL:
        iv = MIN_INTERVAL
    if iv > MAX_INTERVAL:
        iv = MAX_INTERVAL
    return iv


class EdenredConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return EdenredOptionsFlow(config_entry)

    async def async_step_user(self, user_input=None):
        if user_input is not None:

            # Garantir unique_id → impede duplicação futura
            await self.async_set_unique_id(user_input[CONF_EMAIL].lower())
            self._abort_if_unique_id_configured()

            user_input[CONF_INTERVAL] = _sanitize_interval(
                user_input.get(CONF_INTERVAL, 60),
                default=60
            )

            return self.async_create_entry(
                title="Edenred Portugal",
                data=user_input
            )

        data_schema = vol.Schema({
            vol.Required(CONF_EMAIL): str,
            vol.Required(CONF_PASSWORD): str,
            vol.Required(CONF_INTERVAL, default=60):
                vol.All(int, vol.Range(min=MIN_INTERVAL, max=MAX_INTERVAL))
        })

        return self.async_show_form(step_id="user", data_schema=data_schema)


class EdenredOptionsFlow(config_entries.OptionsFlow):

    def __init__(self, config_entry):
        self._config_entry = config_entry   # ← CORREÇÃO

    async def async_step_init(self, user_input=None):

        current = self._config_entry.options.get(
            CONF_INTERVAL,
            self._config_entry.data.get(CONF_INTERVAL, 60)
        )
        current = _sanitize_interval(current, default=60)

        if user_input is not None:
            new_interval = _sanitize_interval(
                user_input.get(CONF_INTERVAL, current),
                default=current
            )

            return self.async_create_entry(
                title="Opções",
                data={CONF_INTERVAL: new_interval}
            )

        data_schema = vol.Schema({
            vol.Required(CONF_INTERVAL, default=current):
                vol.All(int, vol.Range(min=MIN_INTERVAL, max=MAX_INTERVAL))
        })

        return self.async_show_form(step_id="init", data_schema=data_schema)
