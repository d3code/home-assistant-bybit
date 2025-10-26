# Home Assistant Bybit Integration

A Home Assistant custom integration to monitor cryptocurrency ticker data from Bybit using their public WebSocket API.

[![GitHub release](https://img.shields.io/github/release/d3code/home-assistant-bybit.svg)](https://github.com/d3code/home-assistant-bybit/releases)
[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg)](https://github.com/hacs/integration)

## Features

- Real-time cryptocurrency price monitoring via WebSocket
- Support for multiple trading pairs (BTCUSDT, ETHUSDT, etc.)
- Tracks the following data for each pair:
  - Last Price
  - 24h Price Change (%)
  - 24h Volume
  - Open Interest
- Automatic reconnection handling
- UI-based configuration through Home Assistant
- Full precision support (up to 8 decimal places)

## Installation

### Option 1: HACS (Recommended)

1. Install [HACS](https://hacs.xyz/) if you haven't already
2. Go to HACS → Integrations
3. Click on the three dots in the top right corner
4. Select "Custom repositories"
5. Add this repository:
   - Repository: `https://github.com/d3code/home-assistant-bybit`
   - Category: Integration
6. Click "Add"
7. In the Integrations screen, search for "Bybit"
8. Click "Install"
9. Restart Home Assistant

### Option 2: Manual Installation

1. Copy the `custom_components/bybit` folder to your Home Assistant `custom_components` directory
2. Restart Home Assistant
3. The integration will be available to add through the UI

## Configuration

1. Go to **Settings** → **Devices & Services**
2. Click **Add Integration**
3. Search for **Bybit** and select it
4. Enter your trading pairs as comma-separated values (e.g., `BTCUSDT,ETHUSDT,SOLUSDT`)
5. Click **Submit**

### Trading Pair Format

Trading pairs should be in the format: `SYMBOLUSDT` (e.g., BTCUSDT, ETHUSDT, SOLUSDT)

## Usage

After configuration, you'll have sensor entities for each trading pair and metric:

- `sensor.btcusdt_last_price` - Last BTC/USDT price
- `sensor.btcusdt_24h_change` - 24h price change percentage
- `sensor.btcusdt_24h_volume` - 24h volume
- `sensor.btcusdt_open_interest` - Open interest

Each sensor also includes all metrics as attributes for easy access in automations.

## Example Automation

```yaml
automation:
  - alias: "BTC Price Alert"
    trigger:
      - platform: numeric_state
        entity_id: sensor.btcusdt_last_price
        above: 50000
    action:
      - service: notify.mobile_app
        data:
          message: "BTC price is above $50,000!"
          data:
            actions:
              - action: "open_url"
                title: "View on Bybit"
                url: "https://www.bybit.com/trade/usdt/BTCUSDT"
```

## Troubleshooting

If sensors don't update:

1. Check the Home Assistant logs for errors
2. Verify your trading pair symbols are correct
3. Try restarting Home Assistant
4. Check that the Bybit WebSocket is accessible from your network

## Development

This integration uses:

- `websockets` library for WebSocket communication
- Bybit Public Linear WebSocket API: `wss://stream.bybit.com/v5/public/linear`
- Home Assistant's DataUpdateCoordinator for data management

## License

MIT License

## Support

For issues and feature requests, please open an issue on GitHub.
