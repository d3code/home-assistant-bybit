"""The Bybit integration."""
from __future__ import annotations

import asyncio
import json
import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
import websockets

from .const import BYBIT_WS_URL, DOMAIN

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[str] = ["sensor"]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Bybit from a config entry."""
    
    # Get symbols from config
    symbols = entry.data.get("symbols", [])
    
    # Create coordinator
    coordinator = BybitDataUpdateCoordinator(hass, symbols)
    
    # Fetch initial data so we have data when the entities are added
    await coordinator.async_refresh()
    
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator
    
    # Setup sensor platform
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    
    # Start the WebSocket listener
    asyncio.create_task(coordinator.websocket_listener())
    
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    
    if unload_ok:
        coordinator: BybitDataUpdateCoordinator = hass.data[DOMAIN].pop(entry.entry_id)
        coordinator.stop = True
        if coordinator.websocket:
            await coordinator.websocket.close()
    
    return unload_ok


class BybitDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching Bybit data from WebSocket."""
    
    def __init__(self, hass: HomeAssistant, symbols: list[str]) -> None:
        """Initialize."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
        )
        
        self.symbols = symbols
        self.websocket = None
        self.stop = False
        self.data = {}
        
        # Initialize data for each symbol
        for symbol in symbols:
            self.data[symbol] = {
                "last_price": None,
                "24h_change": None,
                "24h_volume": None,
                "open_interest": None,
            }
    
    async def async_refresh(self) -> None:
        """Refresh data - no-op since we use real-time updates."""
        pass
    
    async def websocket_listener(self) -> None:
        """Listen to WebSocket and update coordinator data."""
        reconnect_delay = 5
        
        while not self.stop:
            try:
                _LOGGER.info("Connecting to Bybit WebSocket...")
                
                async with websockets.connect(BYBIT_WS_URL) as websocket:
                    self.websocket = websocket
                    
                    # Subscribe to tickers for all symbols
                    subscribe_msg = {
                        "op": "subscribe",
                        "args": [f"tickers.{symbol}" for symbol in self.symbols]
                    }
                    await websocket.send(json.dumps(subscribe_msg))
                    _LOGGER.info(f"Subscribed to tickers: {self.symbols}")
                    
                    # Reset reconnect delay on successful connection
                    reconnect_delay = 5
                    
                    # Listen for messages
                    async for message in websocket:
                        if self.stop:
                            break
                        
                        try:
                            data = json.loads(message)
                            
                            # Handle ticker updates
                            if "topic" in data and data["topic"].startswith("tickers."):
                                await self._handle_ticker_update(data)
                        
                        except json.JSONDecodeError:
                            _LOGGER.warning(f"Failed to parse message: {message}")
                        except Exception as e:
                            _LOGGER.error(f"Error processing message: {e}")
                
                self.websocket = None
            
            except websockets.exceptions.ConnectionClosed:
                _LOGGER.warning("WebSocket connection closed")
            except Exception as e:
                _LOGGER.error(f"WebSocket error: {e}")
            
            if not self.stop:
                _LOGGER.info(f"Reconnecting in {reconnect_delay} seconds...")
                await asyncio.sleep(reconnect_delay)
                reconnect_delay = min(reconnect_delay * 2, 60)  # Exponential backoff, max 60s
    
    async def _handle_ticker_update(self, data: dict[str, Any]) -> None:
        """Handle ticker update message."""
        try:
            topic = data.get("topic", "")
            symbol = topic.replace("tickers.", "").upper()
            
            if symbol not in self.symbols:
                return
            
            # Bybit sends data in a nested structure
            payload = data.get("data", {})
            if isinstance(payload, list) and len(payload) > 0:
                ticker_data = payload[0]
            else:
                ticker_data = payload
            
            # Only update fields that are present - don't overwrite with 0
            if "lastPrice" in ticker_data:
                self.data[symbol]["last_price"] = float(ticker_data.get("lastPrice"))
            if "price24hPcnt" in ticker_data:
                self.data[symbol]["24h_change"] = float(ticker_data.get("price24hPcnt")) * 100  # Convert to percentage
            if "turnover24h" in ticker_data:
                self.data[symbol]["24h_volume"] = float(ticker_data.get("turnover24h"))
            if "openInterest" in ticker_data:
                self.data[symbol]["open_interest"] = float(ticker_data.get("openInterest"))
            
            # Notify listeners
            self.async_set_updated_data(self.data)
            
            _LOGGER.debug(f"Updated {symbol}: {self.data[symbol]}")
        
        except (ValueError, KeyError, TypeError) as e:
            _LOGGER.error(f"Error parsing ticker data: {e}")
