# HACS Integration Guide for Wattbox

## Overview

This guide outlines the requirements and structure for creating a HACS (Home Assistant Community Store) integration for Wattbox power management systems.

## Repository Structure Requirements

### Critical Rules
- **Single Integration per Repository**: Only one integration per repository
- **File Placement**: All files must be in `custom_components/INTEGRATION_NAME/` directory
- **No Multiple Integrations**: Cannot have multiple subdirectories under `custom_components/`

### Correct Structure
```
custom_components/wattbox/
├── __init__.py
├── sensor.py
├── switch.py
├── config_flow.py
├── manifest.json
├── hacs.json
└── README.md
```

### Incorrect Examples

**❌ Files in root without custom_components/**
```
wattbox/
├── __init__.py
├── sensor.py
├── manifest.json
├── hacs.json
└── README.md
```

**❌ Multiple integrations in one repo**
```
custom_components/
├── wattbox/
│   ├── __init__.py
│   └── manifest.json
└── another_integration/
    ├── __init__.py
    └── manifest.json
```

**❌ Files scattered in root (unless content_in_root: true)**
```
__init__.py
sensor.py
manifest.json
README.md
hacs.json
```

## Essential Files

### 1. manifest.json (Required)

Must include these minimum keys:

```json
{
  "domain": "wattbox",
  "name": "Wattbox",
  "documentation": "https://github.com/yourusername/hass-wattbox",
  "issue_tracker": "https://github.com/yourusername/hass-wattbox/issues",
  "codeowners": ["@yourusername"],
  "version": "1.0.0",
  "requirements": [],
  "dependencies": [],
  "iot_class": "local_polling"
}
```

**Key Fields Explained:**
- `domain`: Unique identifier for the integration
- `name`: Display name in Home Assistant
- `documentation`: Link to integration docs
- `issue_tracker`: Link to issue tracker
- `codeowners`: GitHub usernames of maintainers
- `version`: Current version (semantic versioning)
- `requirements`: Python package dependencies
- `dependencies`: Home Assistant integrations this depends on
- `iot_class`: How the integration communicates (local_polling, cloud_polling, etc.)

### 2. hacs.json (Required for HACS)

```json
{
  "name": "Wattbox",
  "content_in_root": false,
  "filename": "wattbox",
  "country": ["US"],
  "homeassistant": "2023.1.0"
}
```

**Fields Explained:**
- `name`: Display name in HACS
- `content_in_root`: Whether files are in root or custom_components/
- `filename`: Integration directory name
- `country`: Supported countries
- `homeassistant`: Minimum HA version required

## Development Tools & Templates

### 1. Cookiecutter Template (Recommended)
Use [cookiecutter-homeassistant-custom-component](https://github.com/oncleben31/cookiecutter-homeassistant-custom-component) to generate initial structure:

```bash
pip install cookiecutter
cookiecutter https://github.com/oncleben31/cookiecutter-homeassistant-custom-component
```

### 2. Reference Templates
- [integration_blueprint](https://github.com/home-assistant/integration_blueprint) - Official HA template
- [blueprint](https://github.com/custom-components/blueprint) - Community template

## Additional Requirements

### 1. Home Assistant Brands
- Add integration to [home-assistant/brands](https://github.com/home-assistant/brands) repository
- Ensures UI consistency in Home Assistant
- Required for proper icon and branding display

### 2. GitHub Releases (Optional but Recommended)
- Publish releases for better user experience
- HACS shows 5 latest releases for users to choose from
- Use semantic versioning (e.g., v1.0.0, v1.0.1)

## Wattbox-Specific Considerations

### Expected Components
Based on Wattbox power management systems:

1. **Sensors**
   - Power consumption per outlet
   - Voltage readings
   - Current readings
   - Temperature (if supported)
   - Uptime/status

2. **Switches**
   - Individual outlet control
   - Master power control
   - Scheduled power control

3. **Binary Sensors**
   - Outlet status (on/off)
   - Error conditions
   - Network connectivity

4. **Configuration Flow**
   - IP address/hostname setup
   - Authentication (if required)
   - Device discovery

### API Research Needed
- Wattbox web interface endpoints
- Authentication methods
- Data formats (JSON, XML, etc.)
- Polling intervals
- Error handling

## Development Workflow

### Phase 1: Setup
1. Create GitHub repository
2. Use cookiecutter to generate structure
3. Set up development environment
4. Research Wattbox API/interface

### Phase 2: Core Development
1. Implement configuration flow
2. Create basic sensors and switches
3. Add error handling and logging
4. Test with actual Wattbox device

### Phase 3: Polish & Submission
1. Add comprehensive error handling
2. Write documentation
3. Add to Home Assistant brands
4. Create GitHub releases
5. Submit to HACS

## File Structure Deep Dive

### Core Python Files

#### `__init__.py`
- Main integration setup
- Platform loading
- Configuration validation

#### `config_flow.py`
- User-friendly setup process
- Data validation
- Error handling

#### `sensor.py`
- Power monitoring sensors
- Voltage/current readings
- Status information

#### `switch.py`
- Outlet control
- Power management
- Toggle functionality

### Optional Files

#### `const.py`
- Constants and configuration
- Default values
- API endpoints

#### `coordinator.py`
- Data update coordinator
- Centralized data management
- Error handling

#### `strings.json`
- UI text and translations
- Error messages
- User-facing strings

## Testing Requirements

### Local Testing
- Test with actual Wattbox device
- Verify all sensors and switches work
- Test error conditions
- Validate configuration flow

### Integration Testing
- Test with different HA versions
- Verify HACS installation process
- Test update mechanisms

## Resources

### Documentation
- [HACS Integration Docs](https://www.hacs.xyz/docs/publish/integration/)
- [Home Assistant Developer Docs](https://developers.home-assistant.io/docs/creating_component_index/)
- [Home Assistant Brands](https://github.com/home-assistant/brands)

### Tools
- [Cookiecutter Template](https://github.com/oncleben31/cookiecutter-homeassistant-custom-component)
- [Integration Blueprint](https://github.com/home-assistant/integration_blueprint)

### Community
- [Home Assistant Discord](https://discord.gg/c5DvZ4e)
- [HACS Discord](https://discord.gg/hacs)
- [Home Assistant Community Forum](https://community.home-assistant.io/)

## Next Steps

1. **Research Wattbox API** - Understand device communication
2. **Set up development environment** - Install tools and dependencies
3. **Generate initial structure** - Use cookiecutter template
4. **Implement basic functionality** - Start with configuration flow
5. **Test with real device** - Validate functionality
6. **Polish and submit** - Final testing and HACS submission

---

*This guide is based on HACS documentation and Home Assistant development best practices as of 2024.*
