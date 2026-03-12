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

        # Categoria e abreviatura (cat) do último movimento
        latest_category = (latest.get("category") or {}).get("description")
        latest_cat = self._cat_abbrev(latest_category)

        # Parse e formatação de data/hora para o último movimento
        latest_dt = self._parse_transaction_dt(latest.get("transactionDate"))
        latest_formats = self._format_dt(latest_dt)

        # Limpeza do texto
        latest_desc = self._clean_description(latest.get("transactionName", ""))

        # Lista completa formatada
        movements: list[dict[str, Any]] = []
        for mov in mov_list:
            mov_category = (mov.get("category") or {}).get("description")
            mov_cat = self._cat_abbrev(mov_category)

            mov_dt = self._parse_transaction_dt(mov.get("transactionDate"))
            mov_formats = self._format_dt(mov_dt)

            movements.append(
                {
                    # raw original (mantido)
                    "transactionDate": mov.get("transactionDate"),

                    # data/hora formatados
                    "data": mov_formats["data"],
                    "hora": mov_formats["hora"],
                    "data_hora": mov_formats["data_hora"],
                    "timestamp": mov_formats["timestamp"],

                    # categoria + abreviatura
                    "category": mov_category,
                    "cat": mov_cat,

                    # restantes
                    "description": self._clean_description(mov.get("transactionName", "")),
                    "amount": mov.get("amount"),
                    "balance_after": mov.get("balance"),
                }
            )

        return {
            # raw original (mantido)
            "transactionDate": latest.get("transactionDate"),

            # data/hora
            "data": latest_formats["data"],
            "hora": latest_formats["hora"],
            "data_hora": latest_formats["data_hora"],
            "timestamp": latest_formats["timestamp"],

            # categoria + abreviatura
            "category": latest_category,
            "cat": latest_cat,

            # restantes
            "description": latest_desc,
            "balance_after": latest.get("balance"),

            # lista completa
            "movements": movements,
        }

    @staticmethod
    def _clean_description(text: str) -> str:
        """Remove prefixo 'Compra:' (case-insensitive) e espaços repetidos; trim final."""
        t = text or ""
        if t.lower().startswith("compra:"):
            t = t[7:]
        t = re.sub(r"\s+", " ", t).strip()
        return t

    @staticmethod
    def _remove_accents(text: str) -> str:
        """Remove acentos de uma string."""
        normalized = unicodedata.normalize("NFD", text)
        return "".join(ch for ch in normalized if unicodedata.category(ch) != "Mn")

    @classmethod
    def _cat_abbrev(cls, category: str | None) -> str | None:
        """Abreviatura (3 letras) em maiúsculas, SEM acentos.
        Exceção: 'Crédito' -> 'CRD'
        """
        if not category:
            return None

        c = category.strip()
        if not c:
            return None

        # remover acentos e normalizar para uppercase
        c_norm = cls._remove_accents(c).strip().upper()

        # regra especial
        if c_norm == "CREDITO":
            return "CRD"

        return c_norm[:3]

    def _parse_transaction_dt(self, value: str | None) -> datetime | None:
        """
        Faz parse do transactionDate vindo da Edenred (ex: 2026-03-08T19:41:50.642+0000)
        e converte para timezone local do Home Assistant.
        """
        if not value:
            return None

        # Alguns registos podem vir com ou sem milissegundos.
        for fmt in ("%Y-%m-%dT%H:%M:%S.%f%z", "%Y-%m-%dT%H:%M:%S%z"):
            try:
                dt = datetime.strptime(value, fmt)
                return dt_util.as_local(dt)
            except ValueError:
                continue

        return None

    @staticmethod
    def _format_dt(dt: datetime | None) -> dict[str, Any]:
        """Devolve data/hora/data_hora e timestamp (epoch) no formato pedido."""
        if dt is None:
            return {"data": None, "hora": None, "data_hora": None, "timestamp": None}

        data = dt.strftime("%d-%m-%Y")
        hora = dt.strftime("%H:%M")
        data_hora = f"{data} {hora}"
        ts = int(dt.timestamp())

        return {"data": data, "hora": hora, "data_hora": data_hora, "timestamp": ts}
    
