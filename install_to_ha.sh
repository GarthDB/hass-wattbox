#!/bin/bash

# Wattbox Integration Installation Script
# This script helps install the Wattbox integration to your Home Assistant instance

set -e

echo "🔌 Wattbox Integration Installation Script"
echo "=========================================="

# Check if HA_CONFIG_PATH is set
if [ -z "$HA_CONFIG_PATH" ]; then
    echo "❌ Error: HA_CONFIG_PATH environment variable not set"
    echo ""
    echo "Please set your Home Assistant config path:"
    echo "export HA_CONFIG_PATH=/path/to/your/ha/config"
    echo ""
    echo "Common locations:"
    echo "  - Docker: /config (if mounted)"
    echo "  - Home Assistant OS: /config"
    echo "  - Home Assistant Core: ~/.homeassistant"
    echo "  - Home Assistant Supervised: /usr/share/hassio/homeassistant"
    echo ""
    exit 1
fi

# Check if the config directory exists
if [ ! -d "$HA_CONFIG_PATH" ]; then
    echo "❌ Error: Home Assistant config directory not found: $HA_CONFIG_PATH"
    exit 1
fi

# Check if custom_components directory exists, create if not
if [ ! -d "$HA_CONFIG_PATH/custom_components" ]; then
    echo "📁 Creating custom_components directory..."
    mkdir -p "$HA_CONFIG_PATH/custom_components"
fi

# Copy the integration
echo "📦 Copying Wattbox integration..."
cp -r custom_components/wattbox "$HA_CONFIG_PATH/custom_components/"

echo "✅ Installation complete!"
echo ""
echo "Next steps:"
echo "1. Restart Home Assistant"
echo "2. Go to Settings → Devices & Services"
echo "3. Click 'Add Integration'"
echo "4. Search for 'Wattbox'"
echo "5. Enter your device details:"
echo "   - Host: IP address of your Wattbox device"
echo "   - Username: wattbox (default)"
echo "   - Password: wattbox (default)"
echo "   - Polling Interval: 30 seconds (default)"
echo ""
echo "For testing without a real device, you can use:"
echo "  - Host: 192.168.1.100 (or any IP)"
echo "  - Username: wattbox"
echo "  - Password: wattbox"
echo ""
echo "Note: The integration will show connection errors without a real device,"
echo "but you can still take screenshots of the configuration flow and UI."
