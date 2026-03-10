from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN
import re

async def async_setup_entry(hass, entry, async_add_entities):
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator = data["coordinator"]

    entities = []
    for card_id in coordinator.data.keys():
        entities.append(EdenredBalanceSensor(coordinator, card_id))
        entities.append(EdenredLastMovementSensor(coordinator, card_id))

    async_add_entities(entities)

class EdenredBalanceSensor(CoordinatorEntity, SensorEntity):
    _attr_icon = "mdi:credit-card"
    _attr_native_unit_of_measurement = "EUR"

    def __init__(self, coordinator, card_id):
        super().__init__(coordinator)
        self.card_id = card_id
        self._attr_name = f"Edenred {card_id} Saldo"
        self._attr_unique_id = f"edenred_{card_id}_balance"

    @property
    def native_value(self):
        return self.coordinator.data[self.card_id]["details"]["account"]["availableBalance"]

class EdenredLastMovementSensor(CoordinatorEntity, SensorEntity):
    _attr_icon = "mdi:swap-horizontal"
    _attr_native_unit_of_measurement = "EUR"

    def __init__(self, coordinator, card_id):
        super().__init__(coordinator)
        self.card_id = card_id
        self._attr_name = f"Edenred {card_id} Último Movimento"
        self._attr_unique_id = f"edenred_{card_id}_last_movement"

    @property
    def native_value(self):
        mov = self.coordinator.data[self.card_id]["details"].get("movementList", [])
        if mov:
            return mov[0]["amount"]
        return None

    @property
    def extra_state_attributes(self):
        mov = self.coordinator.data[self.card_id]["details"].get("movementList", [])
        if not mov:
            return None

        m = mov[0]
        category = (m.get("category") or {}).get("description")

        raw = m.get("transactionName", "")

        if raw.lower().startswith("compra:"):
            raw = raw[7:]

        raw = re.sub(r"\s+", " ", raw).strip()

        return {
            "date": m.get("transactionDate"),
            "description": raw,
            "category": category,
            "balance_after": m.get("balance"),
        }
