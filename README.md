# Home Assistant Wattbox Integration

[![CI](https://github.com/GarthDB/ha-wattbox/workflows/CI/badge.svg)](https://github.com/GarthDB/ha-wattbox/actions)
[![codecov](https://codecov.io/gh/GarthDB/ha-wattbox/branch/main/graph/badge.svg)](https://codecov.io/gh/GarthDB/ha-wattbox)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Home Assistant](https://img.shields.io/badge/Home%20Assistant-2023.1.0+-blue.svg)](https://www.home-assistant.io/)
[![HACS](https://img.shields.io/badge/HACS-Default-orange.svg)](https://github.com/hacs/integration)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A modern Home Assistant integration for SnapAV Wattbox 800 series power management devices using telnet communication.

> **Status**: ✅ Production Ready - See coverage badge above for current test coverage

## Screenshots

### HACS Discovery
![HACS Discovery](docs/screenshots/01-hacs-discovery.png)

### Setup Process
![Setup Process](docs/screenshots/02-setup-process.png)

### Installation Success
![Installation Success](docs/screenshots/03-installation-success.png)

### Device Integration
![Device Integration](docs/screenshots/04-device-integration.png)

### Control Entities
![Control Entities](docs/screenshots/05-control-entities.png)

### Monitoring Entities
![Monitoring Entities](docs/screenshots/06-monitoring-entities.png)

## Why This Integration?

While there is an existing [hass-wattbox integration](https://github.com/eseglem/hass-wattbox/), this implementation provides several key improvements:

### **Modern Architecture**
- **UI Configuration**: Easy setup through Home Assistant UI vs. YAML-only configuration
- **Config Flow**: Proper integration setup wizard with validation
- **Modern Patterns**: Built using current Home Assistant integration standards

### **Enhanced Features**
- **Comprehensive Entity Support**: More sensor types and better entity organization
- **Robust Error Handling**: Graceful handling of connection issues and device unavailability
- **Real-time Updates**: Live data with proper coordinator pattern
- **Better Device Management**: Improved device info and entity relationships

### **Development Quality**
- **Extensive Testing**: 110+ tests with 82%+ coverage vs. limited testing
- **Active Maintenance**: Regular updates and bug fixes
- **Code Quality**: Modern Python patterns, type hints, and comprehensive linting
- **Documentation**: Detailed setup guides and troubleshooting

### **User Experience**
- **Easier Setup**: No YAML configuration required
- **Better Integration**: Proper device registry and entity organization
- **Reliable Operation**: Robust error handling and recovery
- **Future-Proof**: Built on modern Home Assistant patterns

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
3. Click "+ Explore & Download Repositories"
4. Search for "Wattbox"
5. Click "Download"
6. Restart Home Assistant

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

## ⚠️ Upgrading from v0.2.x to v0.3.0

**Version 0.3.0 introduces a breaking change** to improve entity naming and prevent conflicts with other integrations.

### What Changed

Entity IDs are now properly namespaced with your device name to avoid conflicts:

**Before (v0.2.x):**
- `sensor.voltage` ❌
- `switch.outlet_1` ❌  
- `binary_sensor.device_status` ❌

**After (v0.3.0):**
- `sensor.wattbox_voltage` ✅ (or `sensor.<your_device_name>_voltage`)
- `switch.wattbox_outlet_1` ✅
- `binary_sensor.wattbox_device_status` ✅

### Migration Steps

1. **Before upgrading**, document your existing automations and dashboards that use Wattbox entities
2. **Upgrade** to v0.3.0 through HACS
3. **Restart** Home Assistant
4. **Update** your automations and dashboards with the new entity IDs
5. **Remove** old entities if they weren't automatically cleaned up (Settings > Devices & Services > Entities)

### Finding New Entity IDs

The new entity IDs use your device's hostname as configured in the Wattbox device itself. To find your new entity IDs:

1. Go to Settings > Devices & Services
2. Click on your Wattbox integration
3. View all entities to see their new IDs

**Tip:** Use Home Assistant's search and replace feature in automations to quickly update entity IDs.

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

## Dashboard Examples

Here are some example dashboard configurations to help you get started with visualizing and controlling your Wattbox device.

### Complete Wattbox Dashboard

A comprehensive dashboard showing all device information and controls:

```yaml
type: vertical-stack
cards:
  # Device Status Overview
  - type: horizontal-stack
    cards:
      - type: entity
        entity: binary_sensor.wattbox_device_status
        name: Status
      - type: entity
        entity: binary_sensor.wattbox_power_lost
        name: Power Lost
      - type: entity
        entity: binary_sensor.wattbox_safe_voltage
        name: Safe Voltage
      - type: entity
        entity: binary_sensor.wattbox_cloud_connectivity
        name: Cloud Status

  # Power Monitoring Gauges
  - type: horizontal-stack
    cards:
      - type: gauge
        entity: sensor.wattbox_voltage
        name: Voltage
        min: 100
        max: 130
        severity:
          green: 115
          yellow: 110
          red: 105
        needle: true
      - type: gauge
        entity: sensor.wattbox_current
        name: Current
        min: 0
        max: 20
        needle: true
      - type: gauge
        entity: sensor.wattbox_power
        name: Power
        min: 0
        max: 2000
        needle: true

  # Device Information
  - type: entities
    title: Device Information
    entities:
      - entity: sensor.wattbox_hostname
        name: Hostname
      - entity: sensor.wattbox_model
        name: Model
      - entity: sensor.wattbox_firmware_version
        name: Firmware
      - entity: sensor.wattbox_serial_number
        name: Serial Number

  # Outlet Controls (First 6 outlets as example)
  - type: entities
    title: Outlet Controls
    entities:
      - entity: switch.wattbox_outlet_1
        name: Outlet 1
        icon: mdi:power-socket-us
      - entity: switch.wattbox_outlet_2
        name: Outlet 2
        icon: mdi:power-socket-us
      - entity: switch.wattbox_outlet_3
        name: Outlet 3
        icon: mdi:power-socket-us
      - entity: switch.wattbox_outlet_4
        name: Outlet 4
        icon: mdi:power-socket-us
      - entity: switch.wattbox_outlet_5
        name: Outlet 5
        icon: mdi:power-socket-us
      - entity: switch.wattbox_outlet_6
        name: Outlet 6
        icon: mdi:power-socket-us

  # Master Controls
  - type: entities
    title: Master Controls
    entities:
      - entity: switch.wattbox_master_power
        name: Master Power
        icon: mdi:power
      - entity: switch.wattbox_auto_reboot
        name: Auto Reboot
        icon: mdi:restart
```

### Compact Power Monitoring Card

A simple card focused on power monitoring:

```yaml
type: entities
title: Wattbox Power Monitor
entities:
  - type: attribute
    entity: sensor.wattbox_voltage
    attribute: state
    name: Voltage
    suffix: V
  - type: attribute
    entity: sensor.wattbox_current
    attribute: state
    name: Current
    suffix: A
  - type: attribute
    entity: sensor.wattbox_power
    attribute: state
    name: Power
    suffix: W
  - entity: binary_sensor.wattbox_safe_voltage
    name: Voltage Status
```

### Outlet Grid View

A button card grid for quick outlet control (requires `button-card` from HACS):

```yaml
type: grid
columns: 3
square: false
cards:
  - type: button
    entity: switch.wattbox_outlet_1
    name: Outlet 1
    tap_action:
      action: toggle
    icon: mdi:power-socket-us
  - type: button
    entity: switch.wattbox_outlet_2
    name: Outlet 2
    tap_action:
      action: toggle
    icon: mdi:power-socket-us
  - type: button
    entity: switch.wattbox_outlet_3
    name: Outlet 3
    tap_action:
      action: toggle
    icon: mdi:power-socket-us
  - type: button
    entity: switch.wattbox_outlet_4
    name: Outlet 4
    tap_action:
      action: toggle
    icon: mdi:power-socket-us
  - type: button
    entity: switch.wattbox_outlet_5
    name: Outlet 5
    tap_action:
      action: toggle
    icon: mdi:power-socket-us
  - type: button
    entity: switch.wattbox_outlet_6
    name: Outlet 6
    tap_action:
      action: toggle
    icon: mdi:power-socket-us
```

### Status Banner (Conditional Card)

Show alerts only when there are issues:

```yaml
type: conditional
conditions:
  - condition: or
    conditions:
      - condition: state
        entity: binary_sensor.wattbox_power_lost
        state: "on"
      - condition: state
        entity: binary_sensor.wattbox_safe_voltage
        state: "off"
      - condition: state
        entity: binary_sensor.wattbox_device_status
        state: "off"
card:
  type: markdown
  content: |
    {% if is_state('binary_sensor.wattbox_device_status', 'off') %}
    ⚠️ **Wattbox Offline** - Device not responding
    {% endif %}
    {% if is_state('binary_sensor.wattbox_power_lost', 'on') %}
    🔌 **Power Lost** - Check main power connection
    {% endif %}
    {% if is_state('binary_sensor.wattbox_safe_voltage', 'off') %}
    ⚡ **Voltage Warning** - Voltage outside safe range
    {% endif %}
  card_mod:
    style: |
      ha-card {
        background-color: rgba(255, 152, 0, 0.1);
        border-left: 4px solid orange;
      }
```

### Mini Graph Card (Power History)

Track power consumption over time (requires `mini-graph-card` from HACS):

```yaml
type: custom:mini-graph-card
entities:
  - entity: sensor.wattbox_power
    name: Power Consumption
  - entity: sensor.wattbox_voltage
    name: Voltage
    y_axis: secondary
hours_to_show: 24
points_per_hour: 4
line_width: 2
font_size: 75
show:
  labels: true
  labels_secondary: true
```

## Automation Examples

Here are some useful automation examples for your Wattbox integration.

### Alert on Power Loss

```yaml
automation:
  - alias: "Wattbox: Power Loss Alert"
    trigger:
      - platform: state
        entity_id: binary_sensor.wattbox_power_lost
        to: "on"
    action:
      - service: notify.notify
        data:
          title: "⚠️ Wattbox Power Lost"
          message: "Main power lost to Wattbox at {{ now().strftime('%H:%M:%S') }}"
```

### Voltage Monitoring

```yaml
automation:
  - alias: "Wattbox: Voltage Warning"
    trigger:
      - platform: state
        entity_id: binary_sensor.wattbox_safe_voltage
        to: "off"
    action:
      - service: notify.notify
        data:
          title: "⚡ Wattbox Voltage Warning"
          message: >
            Voltage outside safe range: {{ states('sensor.wattbox_voltage') }}V
```

### Scheduled Equipment Reboot

```yaml
automation:
  - alias: "Wattbox: Weekly Equipment Reboot"
    trigger:
      - platform: time
        at: "03:00:00"
    condition:
      - condition: time
        weekday:
          - sun
    action:
      # Turn off outlet
      - service: switch.turn_off
        target:
          entity_id: switch.wattbox_outlet_1
      # Wait 30 seconds
      - delay:
          seconds: 30
      # Turn on outlet
      - service: switch.turn_on
        target:
          entity_id: switch.wattbox_outlet_1
```

### High Power Usage Alert

```yaml
automation:
  - alias: "Wattbox: High Power Usage"
    trigger:
      - platform: numeric_state
        entity_id: sensor.wattbox_power
        above: 1500
        for:
          minutes: 5
    action:
      - service: notify.notify
        data:
          title: "⚡ High Power Usage"
          message: >
            Wattbox power consumption is {{ states('sensor.wattbox_power') }}W

```

## Development

### Prerequisites

- Python 3.9+
- Home Assistant 2023.1.0+
- Wattbox 800 series device for testing

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/GarthDB/ha-wattbox.git
cd ha-wattbox

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
make test

# Run all checks (linting, formatting, tests)
make check-all

# Format code
make format
```

### Local CI Testing

This project includes `act` CLI support for local GitHub Actions testing:

```bash
# Test the full CI pipeline locally
act -j test

# Test specific Python versions
act -j test -P ubuntu-latest=catthehacker/ubuntu:act-latest
```

### Development Tools

This project includes comprehensive development tooling:

- **Pre-commit Hooks**: Automated code formatting and linting
- **Makefile**: Common development commands (`make test`, `make lint`, `make format`)
- **Local CI Testing**: `act` CLI for testing GitHub Actions locally
- **Code Quality**: Black, isort, flake8, mypy, bandit, safety, vulture
- **Testing**: pytest with comprehensive test coverage
- **CI/CD**: GitHub Actions with multi-Python version testing

### Project Structure

```
ha-wattbox/
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
│       ├── binary_sensor.py
│       ├── telnet_client.py
│       ├── icon.png
│       ├── icon@2x.png
│       ├── logo.png
│       ├── logo@2x.png
│       └── hacs.json
├── docs/
│   ├── screenshots/
│   │   ├── 01-hacs-discovery.png
│   │   ├── 02-setup-process.png
│   │   ├── 03-installation-success.png
│   │   ├── 04-device-integration.png
│   │   ├── 05-control-entities.png
│   │   └── 06-monitoring-entities.png
│   ├── HACS_INTEGRATION_GUIDE.md
│   ├── INTEGRATION_TEST_RESULTS.md
│   └── snapav-2.7.0.4.md
├── tests/
├── .github/workflows/
├── .pre-commit-config.yaml
├── Makefile
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
- Inspired by the [eseglem/hass-wattbox](https://github.com/eseglem/hass-wattbox) integration, but completely rewritten with modern Home Assistant patterns
- Built for the Home Assistant community with focus on reliability and ease of use

## Support

- **Issues**: [GitHub Issues](https://github.com/garthdb/ha-wattbox/issues)
- **Discussions**: [GitHub Discussions](https://github.com/garthdb/ha-wattbox/discussions)
- **Home Assistant Community**: [Community Forum](https://community.home-assistant.io/)

## Changelog

### v0.1.0 (Planned)
- Initial release
- Telnet communication support
- Basic outlet control
- Power monitoring
- HACS compatibility
# Test CI/CD
