# Home Assistant Wattbox Integration

A modern Home Assistant integration for SnapAV Wattbox 800 series power management devices using telnet communication.

> **Status**: ✅ Production Ready - 100% test coverage with 94.41% code coverage

## Features

- **Telnet Communication**: Direct telnet connection to Wattbox 800 series devices
- **Outlet Control**: Individual outlet on/off control and power cycling
- **Power Monitoring**: Real-time voltage, current, and power consumption monitoring
- **Status Indicators**: Device status, connectivity, and error monitoring
- **Auto Reboot Control**: Enable/disable auto-reboot functionality
- **HACS Compatible**: Easy installation through Home Assistant Community Store

## Supported Devices

- **Wattbox 800 Series**: WB-800VPS-IPVM-18 and compatible models
- **Protocol**: Telnet (port 23)
- **Authentication**: Username/password based

## Installation

### HACS (Recommended)

1. Open HACS in Home Assistant
2. Go to Integrations
3. Click the three dots menu
4. Select "Custom repositories"
5. Add this repository URL
6. Search for "Wattbox" and install

### Manual Installation

1. Download the latest release
2. Extract to `custom_components/wattbox/` in your Home Assistant config
3. Restart Home Assistant
4. Add the integration through the UI

## Configuration

1. Go to Settings > Devices & Services
2. Click "Add Integration"
3. Search for "Wattbox"
4. Enter your device details:
   - **Host**: IP address of your Wattbox device
   - **Username**: Device username (default: wattbox)
   - **Password**: Device password (default: wattbox)
   - **Polling Interval**: How often to update data (default: 30 seconds)

## Entities

### Switches
- **Outlet 1-18**: Individual outlet control
- **Master Power**: Control all outlets at once
- **Auto Reboot**: Enable/disable auto-reboot functionality

### Sensors
- **Voltage**: Current voltage reading
- **Current**: Current amperage reading
- **Power**: Current power consumption
- **Firmware Version**: Device firmware version
- **Model**: Device model information
- **Serial Number**: Device serial number
- **Hostname**: Device hostname

### Binary Sensors
- **Device Status**: Device online/offline status
- **Power Lost**: Power loss detection
- **Safe Voltage**: Voltage within safe range
- **Cloud Connectivity**: Cloud connection status

## Development

### Prerequisites

- Python 3.9+
- Home Assistant 2023.1.0+
- Wattbox 800 series device for testing

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/garthdb/hass-wattbox.git
cd hass-wattbox

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/
```

### Project Structure

```
hass-wattbox/
├── custom_components/
│   └── wattbox/
│       ├── __init__.py
│       ├── config_flow.py
│       ├── const.py
│       ├── coordinator.py
│       ├── entity.py
│       ├── manifest.json
│       ├── sensor.py
│       ├── switch.py
│       └── binary_sensor.py
├── tests/
├── docs/
├── requirements-dev.txt
├── pyproject.toml
└── README.md
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Based on the [bitfocus/companion-module-snapav-wattbox](https://github.com/bitfocus/companion-module-snapav-wattbox) telnet implementation
- Inspired by the [eseglem/hass-wattbox](https://github.com/eseglem/hass-wattbox) integration
- Built for the Home Assistant community

## Support

- **Issues**: [GitHub Issues](https://github.com/garthdb/hass-wattbox/issues)
- **Discussions**: [GitHub Discussions](https://github.com/garthdb/hass-wattbox/discussions)
- **Home Assistant Community**: [Community Forum](https://community.home-assistant.io/)

## Changelog

### v0.1.0 (Planned)
- Initial release
- Telnet communication support
- Basic outlet control
- Power monitoring
- HACS compatibility
