"""Sensor platform for Bybit integration."""
from __future__ import annotations

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

from .const import (
    ATTR_24H_CHANGE,
    ATTR_24H_VOLUME,
    ATTR_LAST_PRICE,
    ATTR_OPEN_INTEREST,
    DOMAIN,
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Bybit sensor entities."""
    coordinator: DataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    
    symbols = entry.data.get("symbols", [])
    
    # Create a sensor for each symbol
    sensors = []
    for symbol in symbols:
        sensors.append(BybitTickerSensor(coordinator, symbol, "last_price", "Last Price", "USDT", None))
        sensors.append(BybitTickerSensor(coordinator, symbol, "24h_change", "24h Change", "%", None))
        sensors.append(BybitTickerSensor(coordinator, symbol, "24h_volume", "24h Volume", "USDT", None))
        sensors.append(BybitTickerSensor(coordinator, symbol, "open_interest", "Open Interest", "USDT", None))
    
    async_add_entities(sensors)


class BybitTickerSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Bybit ticker sensor."""
    
    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        symbol: str,
        attribute: str,
        name: str,
        unit: str,
        device_class: SensorDeviceClass | None,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        
        self._symbol = symbol
        self._attribute = attribute
        self._attr_name = f"{symbol} {name}"
        self._attr_unique_id = f"{symbol}_{attribute}"
        self._attr_native_unit_of_measurement = unit
        self._attr_device_class = device_class
        self._attr_state_class = SensorStateClass.MEASUREMENT
        
        # Set up device info
        self._attr_device_info = {
            "identifiers": {(DOMAIN, f"bybit_{symbol}")},
            "name": f"Bybit {symbol}",
            "manufacturer": "Bybit",
            "model": "Ticker Data",
        }
    
    @property
    def native_value(self) -> float | None:
        """Return the state of the sensor."""
        if self.coordinator.data is None:
            return None
        
        symbol_data = self.coordinator.data.get(self._symbol)
        if symbol_data is None:
            return None
        
        return symbol_data.get(self._attribute)
    
    @property
    def extra_state_attributes(self) -> dict[str, any]:
        """Return the state attributes."""
        if self.coordinator.data is None:
            return {}
        
        symbol_data = self.coordinator.data.get(self._symbol)
        if symbol_data is None:
            return {}
        
        attrs = {}
        
        # Include all attributes for the symbol
        if ATTR_LAST_PRICE in symbol_data:
            attrs["last_price"] = symbol_data[ATTR_LAST_PRICE]
        if ATTR_24H_CHANGE in symbol_data:
            attrs["24h_change"] = symbol_data[ATTR_24H_CHANGE]
        if ATTR_24H_VOLUME in symbol_data:
            attrs["24h_volume"] = symbol_data[ATTR_24H_VOLUME]
        if ATTR_OPEN_INTEREST in symbol_data:
            attrs["open_interest"] = symbol_data[ATTR_OPEN_INTEREST]
        
        return attrs
