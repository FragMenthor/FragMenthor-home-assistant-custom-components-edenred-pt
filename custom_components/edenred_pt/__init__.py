
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from datetime import timedelta
import logging

from .const import DOMAIN, CONF_EMAIL, CONF_PASSWORD, CONF_INTERVAL
from .api import EdenredClient

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    email = entry.data[CONF_EMAIL]
    password = entry.data[CONF_PASSWORD]

    interval = entry.options.get(CONF_INTERVAL, entry.data.get(CONF_INTERVAL, 60))

    client = EdenredClient(email, password)

    async def async_update():
        try:
            await client.authenticate()
            card_list = await client.get_cards()
            results = {}
            for card in card_list.get("data", []):
                card_id = card["id"]
                details = await client.get_card_details(card_id)
                results[card_id] = {
                    "card": card,
                    "details": details.get("data", {})
                }
            return results
        except Exception as err:
            raise UpdateFailed(f"Erro ao atualizar: {err}")

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="edenred_pt",
        update_method=async_update,
        update_interval=timedelta(minutes=interval),
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        "client": client,
        "coordinator": coordinator,
    }

    async def handle_force_update(call: ServiceCall):
        _LOGGER.info("Forçando atualização manual da integração Edenred PT…")
        await coordinator.async_request_refresh()

    hass.services.async_register(DOMAIN, "force_update", handle_force_update)

    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    unload = await hass.config_entries.async_unload_platforms(entry, ["sensor"])
    if unload:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload
