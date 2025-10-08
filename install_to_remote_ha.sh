#!/bin/bash

# Wattbox Integration Installation Script for Remote Home Assistant
# This script helps install the Wattbox integration to your remote Home Assistant instance

set -e

echo "🔌 Wattbox Integration Installation Script (Remote HA)"
echo "===================================================="

# Check if required variables are set
if [ -z "$HA_HOST" ] || [ -z "$HA_USER" ]; then
    echo "❌ Error: Required environment variables not set"
    echo ""
    echo "Please set your Home Assistant connection details:"
    echo "export HA_HOST=your-ha-ip-or-hostname"
    echo "export HA_USER=your-username"
    echo ""
    echo "Example:"
    echo "export HA_HOST=192.168.1.100"
    echo "export HA_USER=homeassistant"
    echo ""
    exit 1
fi

# Set default port if not provided
HA_PORT=${HA_PORT:-22}

echo "📡 Connecting to Home Assistant at $HA_HOST:$HA_PORT as $HA_USER"

# Check if we can connect
if ! ssh -o ConnectTimeout=10 -p $HA_PORT $HA_USER@$HA_HOST "echo 'Connection successful'" 2>/dev/null; then
    echo "❌ Error: Cannot connect to Home Assistant"
    echo ""
    echo "Please check:"
    echo "1. Home Assistant is running and accessible"
    echo "2. SSH is enabled on your Home Assistant"
    echo "3. Your SSH key is set up (or use password authentication)"
    echo "4. The IP address and username are correct"
    echo ""
    echo "To enable SSH on Home Assistant:"
    echo "1. Go to Settings → Add-ons → Add-on Store"
    echo "2. Search for 'SSH & Web Terminal'"
    echo "3. Install and configure it"
    echo ""
    exit 1
fi

echo "✅ Connection successful!"

# Create the integration directory on the remote machine
echo "📁 Creating integration directory on remote Home Assistant..."
ssh -p $HA_PORT $HA_USER@$HA_HOST "mkdir -p /config/custom_components"

# Copy the integration files
echo "📦 Copying Wattbox integration files..."
scp -r -P $HA_PORT custom_components/wattbox $HA_USER@$HA_HOST:/config/custom_components/

echo "✅ Installation complete!"
echo ""
echo "Next steps:"
echo "1. Restart Home Assistant (Settings → System → Restart)"
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
echo ""
echo "To take screenshots:"
echo "1. Access Home Assistant via web browser"
echo "2. Follow the screenshot guide in SCREENSHOT_GUIDE.md"
echo "3. Use browser developer tools to capture clean screenshots"
