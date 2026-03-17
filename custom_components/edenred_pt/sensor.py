from __future__ import annotations

import re
import unicodedata
from datetime import datetime
from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util import dt as dt_util

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
    _attr_icon = "mdi:credit-card"
    _attr_native_unit_of_measurement = "EUR"

    def __init__(self, coordinator, card_id: int) -> None:
        super().__init__(coordinator)
        self.card_id = card_id
        self._attr_name = f"Edenred {card_id} Saldo"
        self._attr_unique_id = f"edenred_{card_id}_balance"

    @property
    def native_value(self) -> Any:
        return self.coordinator.data[self.card_id]["details"]["account"]["availableBalance"]

    @property
    def extra_state_attributes(self) -> dict[str, Any] | None:
        card = self.coordinator.data[self.card_id].get("card", {}) or {}
        product = card.get("product") or {}
        return {
            "ownerName": card.get("ownerName"),
            "number": card.get("number"),
            "status": card.get("status"),
            "product_name": product.get("name"),
        }


class EdenredLastMovementSensor(CoordinatorEntity, SensorEntity):
    _attr_icon = "mdi:swap-horizontal"
    _attr_native_unit_of_measurement = "EUR"

    def __init__(self, coordinator, card_id: int) -> None:
        super().__init__(coordinator)
        self.card_id = card_id
        self._attr_name = f"Edenred {card_id} Último Movimento"
        self._attr_unique_id = f"edenred_{card_id}_last_movement"

    @property
    def native_value(self) -> Any:
        """Valor do último movimento != 0."""
        mov_list = self.coordinator.data[self.card_id]["details"].get("movementList", [])
        filtered = [m for m in mov_list if m.get("amount") != 0]

        if not filtered:
            return None  # Sem movimentos válidos

        return filtered[0].get("amount")

    @property
    def extra_state_attributes(self) -> dict[str, Any] | None:
        mov_list = self.coordinator.data[self.card_id]["details"].get("movementList", [])

        # Filtrar movimentos amount != 0
        filtered = [m for m in mov_list if m.get("amount") != 0]

        if not filtered:
            return None

        # Movimento mais recente válido
        latest = filtered[0]

        # Categoria + abreviatura
        latest_category = (latest.get("category") or {}).get("description")
        latest_cat = self._cat_abbrev(latest_category)

        # Tipos
        latest_type = self._movement_type(latest.get("amount"))
        latest_t = self._movement_circle(latest.get("amount"))

        # Datas
        latest_dt = self._parse_transaction_dt(latest.get("transactionDate"))
        latest_formats = self._format_dt(latest_dt)

        # Texto limpo
        latest_desc = self._clean_description(latest.get("transactionName", ""))

        # Lista completa com movimentos ≠ 0
        movements: list[dict[str, Any]] = []
        for mov in filtered:
            mov_category = (mov.get("category") or {}).get("description")
            mov_cat = self._cat_abbrev(mov_category)
            mov_type = self._movement_type(mov.get("amount"))
            mov_t = self._movement_circle(mov.get("amount"))

            mov_dt = self._parse_transaction_dt(mov.get("transactionDate"))
            mov_formats = self._format_dt(mov_dt)

            movements.append(
                {
                    "transactionDate": mov.get("transactionDate"),
                    "date": mov_formats["date"],
                    "time": mov_formats["time"],
                    "date_time": mov_formats["date_time"],
                    "timestamp": mov_formats["timestamp"],
                    "category": mov_category,
                    "cat": mov_cat,
                    "type": mov_type,
                    "symbol": mov_t,
                    "description": self._clean_description(mov.get("transactionName", "")),
                    "amount": mov.get("amount"),
                    "balance_after": mov.get("balance"),
                }
            )

        return {
            "transactionDate": latest.get("transactionDate"),
            "date": latest_formats["date"],
            "time": latest_formats["time"],
            "date_time": latest_formats["date_time"],
            "timestamp": latest_formats["timestamp"],
            "category": latest_category,
            "cat": latest_cat,
            "type": latest_type,
            "symbol": latest_t,
            "description": latest_desc,
            "balance_after": latest.get("balance"),
            "transactions": movements,
        }

    @staticmethod
    def _clean_description(text: str) -> str:
        t = text or ""
        if t.lower().startswith("compra:"):
            t = t[7:]
        return re.sub(r"\s+", " ", t).strip()

    @staticmethod
    def _remove_accents(text: str) -> str:
        normalized = unicodedata.normalize("NFD", text)
        return "".join(ch for ch in normalized if unicodedata.category(ch) != "Mn")

    @classmethod
    def _cat_abbrev(cls, category: str | None) -> str | None:
        if not category:
            return None
        c_norm = cls._remove_accents(category).strip().upper()
        if c_norm == "CREDITO":
            return "CRD"
        return c_norm[:3] if c_norm else None

    @staticmethod
    def _movement_type(amount: float | None) -> str | None:
        if amount is None:
            return None
        return "▲" if amount > 0 else "▼"

    @staticmethod
    def _movement_circle(amount: float | None) -> str | None:
        if amount is None:
            return None
        return "🟢" if amount > 0 else "🔴"

    def _parse_transaction_dt(self, value: str | None) -> datetime | None:
        if not value:
            return None
        for fmt in ("%Y-%m-%dT%H:%M:%S.%f%z", "%Y-%m-%dT%H:%M:%S%z"):
            try:
                dt = datetime.strptime(value, fmt)
                return dt_util.as_local(dt)
            except ValueError:
                continue
        return None

    @staticmethod
    def _format_dt(dt: datetime | None) -> dict[str, Any]:
        if dt is None:
            return {"date": None, "time": None, "date_time": None, "timestamp": None}

        data = dt.strftime("%d-%m-%Y")
        hora = dt.strftime("%H:%M")

        return {
            "date": data,
            "time": hora,
            "date_time": f"{data} {hora}",
            "timestamp": int(dt.timestamp()),
        }
