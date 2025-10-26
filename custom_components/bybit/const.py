"""Constants for the Bybit integration."""

DOMAIN = "bybit"

# WebSocket configuration
BYBIT_WS_URL = "wss://stream.bybit.com/v5/public/linear"

# Default trading pairs
DEFAULT_SYMBOLS = ["BTCUSDT"]

# Sensor attributes
ATTR_LAST_PRICE = "last_price"
ATTR_24H_CHANGE = "24h_change"
ATTR_24H_VOLUME = "24h_volume"
ATTR_OPEN_INTEREST = "open_interest"

# Configuration keys
CONF_SYMBOLS = "symbols"
