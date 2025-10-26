"""Config flow for Bybit integration."""
from __future__ import annotations

import re
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult
import homeassistant.helpers.config_validation as cv

from .const import CONF_SYMBOLS, DEFAULT_SYMBOLS, DOMAIN


def validate_symbols(symbols: str) -> list[str]:
    """Validate and normalize trading pair symbols."""
    # Split by comma and clean up
    symbol_list = [s.strip().upper() for s in symbols.split(",")]
    
    # Validate format (should be LIKE BTCUSDT, ETHUSDT, etc)
    pattern = re.compile(r'^[A-Z]+\w+$')
    valid_symbols = []
    
    for symbol in symbol_list:
        if not symbol:
            continue
        if not pattern.match(symbol):
            raise vol.Invalid(f"Invalid symbol format: {symbol}")
        valid_symbols.append(symbol)
    
    if not valid_symbols:
        raise vol.Invalid("At least one valid trading pair is required")
    
    return valid_symbols


class BybitConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Bybit."""
    
    VERSION = 1
    
    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        
        errors: dict[str, str] = {}
        
        if user_input is not None:
            try:
                # Validate and normalize symbols
                symbols = validate_symbols(user_input[CONF_SYMBOLS])
                
                # Create entry
                return self.async_create_entry(
                    title=f"Bybit ({len(symbols)} symbols)",
                    data={CONF_SYMBOLS: symbols},
                )
            
            except vol.Invalid as err:
                errors["base"] = str(err)
        
        # Show the form
        schema = vol.Schema({
            vol.Required(
                CONF_SYMBOLS,
                default="BTCUSDT",
                description="Trading pairs (comma-separated, e.g., BTCUSDT, ETHUSDT)"
            ): str,
        })
        
        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors=errors,
            description_placeholders={
                "example": "BTCUSDT,ETHUSDT,SOLUSDT"
            }
        )
