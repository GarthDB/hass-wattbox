# Wattbox API Research Summary

## Current State Analysis

### Existing Home Assistant Integration
**Repository**: [eseglem/hass-wattbox](https://github.com/eseglem/hass-wattbox/)
- **Status**: Unmaintained (last update 2 years ago)
- **Dependencies**: Uses `pywattbox>=0.4.0,<0.7.0` library
- **Issues**: 
  - Not compatible with Wattbox 800 series
  - Uses HTTP API instead of telnet
  - Outdated dependencies
  - No per-outlet energy usage reporting for 800 series

### Companion Module Reference
**Repository**: [bitfocus/companion-module-snapav-wattbox](https://github.com/bitfocus/companion-module-snapav-wattbox/)
- **Status**: Active (latest release Dec 19, 2024)
- **Language**: JavaScript (Node.js)
- **Purpose**: Bitfocus Companion integration for Wattbox
- **Value**: Good reference for command structures and device communication

## Wattbox 800 Series API Characteristics

### Communication Protocol
- **Primary**: SSH/Telnet (not HTTP like older models)
- **Port**: Typically 23 (telnet) or 22 (SSH)
- **Authentication**: Username/password based
- **Command Structure**: Text-based commands with specific syntax

### Key Differences from Older Models
1. **API Protocol**: 800 series uses SSH/Telnet, not HTTP
2. **Command Set**: Different command structure than 300/700 series
3. **Energy Reporting**: Limited per-outlet energy usage reporting
4. **Firmware**: Different firmware with updated command set

## API Documentation References

### Official Documentation
- **SnapAV WattBox API v2.4**: Primary reference for command structures
- **Firmware Release Notes**: [8x0 Series FW RN](https://help.snapone.com/wb-8x0-fw/Content/FW%20RN/8x0/8x0%20series%20FW%20RN.htm)
- **Community Discussions**: [Home Assistant Community Forum](https://community.home-assistant.io/t/wattbox-integration/108271?page=5)

### Key Insights from Community
1. **800 Series Specific**: Need to start from scratch for 800 series integration
2. **SSH/Telnet Required**: HTTP API not available on 800 series
3. **Energy Monitoring**: Limited per-outlet energy reporting capabilities
4. **Compatibility**: Existing integrations don't work with 800 series

## Technical Implementation Requirements

### Core Components Needed
1. **Telnet/SSH Client**: Python telnetlib or paramiko for SSH
2. **Command Parser**: Parse device responses and status
3. **Entity Mapping**: Map device outlets to HA switches/sensors
4. **Error Handling**: Robust connection and command error handling
5. **Configuration Flow**: User-friendly setup process

### Expected Entities
Based on existing integration and Wattbox capabilities:

#### Switches
- Individual outlet control (8 outlets typically)
- Master power control
- Auto-reboot toggle
- Mute toggle

#### Sensors
- Voltage readings
- Current readings  
- Power consumption
- Battery status (if UPS equipped)
- Estimated run time (if UPS equipped)

#### Binary Sensors
- Outlet status (on/off)
- Power lost status
- Safe voltage status
- Cloud connectivity status
- Battery health status

## Development Strategy

### Phase 1: Foundation
1. **Research Telnet Commands**: Study API documentation for 800 series
2. **Create Basic Client**: Implement telnet connection and basic commands
3. **Test with Real Device**: Validate commands with actual Wattbox 800

### Phase 2: Core Integration
1. **Generate HACS Structure**: Use cookiecutter template
2. **Implement Configuration Flow**: User-friendly setup
3. **Create Entity Classes**: Switches, sensors, binary sensors
4. **Add Error Handling**: Robust connection management

### Phase 3: Polish & Submission
1. **Comprehensive Testing**: Test all features thoroughly
2. **Documentation**: Clear setup and usage instructions
3. **HACS Submission**: Follow HACS guidelines
4. **Community Feedback**: Engage with HA community

## Next Steps

1. **Examine Companion Module**: Study the JavaScript implementation for command patterns
2. **Test Telnet Commands**: Connect to actual Wattbox 800 and test commands
3. **Create Development Environment**: Set up cookiecutter and development tools
4. **Implement Basic Client**: Start with simple telnet communication
5. **Build HACS Integration**: Create the full Home Assistant integration

## Resources

### Documentation
- [SnapAV WattBox API v2.4](https://manuals.plus/m/5a2b330612ca15048f5f17a0c83393c4cb3a4fea3a82dd2e96e7b8fb7b8fb553)
- [8x0 Series Firmware Release Notes](https://help.snapone.com/wb-8x0-fw/Content/FW%20RN/8x0/8x0%20series%20FW%20RN.htm)

### Existing Code
- [eseglem/hass-wattbox](https://github.com/eseglem/hass-wattbox/) - HA integration (outdated)
- [bitfocus/companion-module-snapav-wattbox](https://github.com/bitfocus/companion-module-snapav-wattbox/) - Companion module

### Community
- [Home Assistant Community Forum - WattBox Integration](https://community.home-assistant.io/t/wattbox-integration/108271?page=5)
- [HACS Integration Guidelines](https://www.hacs.xyz/docs/publish/integration/)

---

*Research completed on January 21, 2025*
