from __future__ import annotations

import re
from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up sensors from a config entry."""
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator = data["coordinator"]

    entities: list[SensorEntity] = []

    # Para cada cartão devolvido pelo coordinator, criamos 2 sensores
    for card_id in coordinator.data.keys():
        entities.append(EdenredBalanceSensor(coordinator, card_id))
        entities.append(EdenredLastMovementSensor(coordinator, card_id))

    async_add_entities(entities)


class EdenredBalanceSensor(CoordinatorEntity, SensorEntity):
    """Sensor de Saldo do Cartão Edenred."""

    _attr_icon = "mdi:credit-card"
    _attr_native_unit_of_measurement = "EUR"

    def __init__(self, coordinator, card_id: int) -> None:
        super().__init__(coordinator)
        self.card_id = card_id
        self._attr_name = f"Edenred {card_id} Saldo"
        self._attr_unique_id = f"edenred_{card_id}_balance"

    @property
    def native_value(self) -> Any:
        """Saldo disponível do cartão."""
        return self.coordinator.data[self.card_id]["details"]["account"]["availableBalance"]

    @property
    def extra_state_attributes(self) -> dict[str, Any] | None:
        """Atributos adicionais do cartão no sensor de saldo."""
        card = self.coordinator.data[self.card_id].get("card", {}) or {}
        product = card.get("product") or {}
        return {
            "ownerName": card.get("ownerName"),
            "number": card.get("number"),
            "status": card.get("status"),
            # Evitamos ponto no nome do atributo (não suportado): usamos product_name
            "product_name": product.get("name"),
        }


class EdenredLastMovementSensor(CoordinatorEntity, SensorEntity):
    """Sensor do Último Movimento do Cartão Edenred."""

    _attr_icon = "mdi:swap-horizontal"
    _attr_native_unit_of_measurement = "EUR"

    def __init__(self, coordinator, card_id: int) -> None:
        super().__init__(coordinator)
        self.card_id = card_id
        self._attr_name = f"Edenred {card_id} Último Movimento"
        self._attr_unique_id = f"edenred_{card_id}_last_movement"

    @property
    def native_value(self) -> Any:
        """Valor (amount) do último movimento."""
        mov = self.coordinator.data[self.card_id]["details"].get("movementList", [])
        if mov:
            return mov[0].get("amount")
        return None

    @property
    def extra_state_attributes(self) -> dict[str, Any] | None:
        """Atributos: data/descrição limpa/categoria/balance_after + lista completa de movimentos."""
        mov_list = self.coordinator.data[self.card_id]["details"].get("movementList", [])
        if not mov_list:
            return None

        # Movimento mais recente
        latest = mov_list[0]

        # --- Limpeza do texto (remove "Compra:" + espaços repetidos) ---
        latest_desc = self._clean_description(latest.get("transactionName", ""))

        # Lista completa formatada
        movements: list[dict[str, Any]] = []
        for mov in mov_list:
            movements.append(
                {
                    "date": mov.get("transactionDate"),
                    "description": self._clean_description(mov.get("transactionName", "")),
                    "amount": mov.get("amount"),
                    "category": (mov.get("category") or {}).get("description"),
                    "balance_after": mov.get("balance"),
                }
            )

        return {
            "date": latest.get("transactionDate"),
            "description": latest_desc,
            "category": (latest.get("category") or {}).get("description"),
            "balance_after": latest.get("balance"),
            "movements": movements,
        }

    @staticmethod
    def _clean_description(text: str) -> str:
        """Remove prefixo 'Compra:' (case-insensitive) e espaços repetidos; trim final."""
        t = text or ""
        # remover prefixo "Compra:" (com exatidão; sem afetar outros textos)
        if t.lower().startswith("compra:"):
            t = t[7:]
        # normalizar espaços repetidos
        t = re.sub(r"\s+", " ", t).strip()
        return t
