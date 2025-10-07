# Python Libraries Research - Wattbox Control

## Summary of Findings

After extensive research, I've identified several Python libraries and tools for controlling Wattbox devices, though accessing the actual source code has been challenging.

## Identified Libraries

### 1. pywattbox (Primary Library)
- **Source**: PyPI package
- **Latest Version**: 0.9.0 (released May 7, 2025)
- **Status**: Actively maintained
- **Documentation**: References [hass-wattbox](https://github.com/eseglem/hass-wattbox) for usage examples
- **Compatibility**: Unknown with 800 series
- **Protocol**: Likely HTTP-based (based on existing HA integration)

### 2. pywattbox by gjbadros
- **Source**: GitHub repository
- **Status**: Less active, limited information available
- **Purpose**: Polling interactions with SnapAV WattBox IP-controlled outlets
- **Protocol**: Unknown

### 3. wattbox-api (Node.js)
- **Source**: NPM package
- **Language**: JavaScript/Node.js
- **Support**: WB-800, WB-250, WB-150 series
- **Protocol**: Unknown
- **Value**: Good reference for API patterns

## Current State Analysis

### Existing Home Assistant Integration
- **Repository**: [eseglem/hass-wattbox](https://github.com/eseglem/hass-wattbox/)
- **Dependencies**: `pywattbox>=0.4.0,<0.7.0`
- **Status**: Unmaintained (2 years old)
- **Issues**: 
  - Not compatible with 800 series
  - Uses HTTP protocol
  - Version constraint conflicts with newer pywattbox

### Version Compatibility Issues
- **Current HA Integration**: Requires pywattbox 0.4.0-0.7.0
- **Latest pywattbox**: 0.9.0 (May 2025)
- **Gap**: 0.7.0 to 0.9.0 - potential breaking changes
- **Risk**: Newer versions may not be compatible with existing integration

## Key Insights

### 1. Library Limitations
- **No Telnet Support**: Existing libraries appear to use HTTP protocol
- **800 Series Compatibility**: Unclear if any library supports 800 series
- **Version Conflicts**: Existing HA integration has strict version constraints

### 2. Protocol Mismatch
- **Companion Module**: Uses telnet for 250 series, HTTP for others
- **Python Libraries**: Appear to use HTTP only
- **800 Series**: Requires telnet/SSH (not HTTP)

### 3. Development Gap
- **No Modern Telnet Library**: No Python library found with telnet support
- **Outdated Integration**: Existing HA integration is 2 years old
- **Version Conflicts**: Newer pywattbox versions may break existing integration

## Recommendations

### Option 1: Build Custom Telnet Client
**Pros:**
- Full control over implementation
- Direct telnet support for 800 series
- No dependency on outdated libraries
- Can implement exactly what we need

**Cons:**
- More development work
- Need to implement all functionality from scratch
- No community support initially

### Option 2: Extend Existing pywattbox
**Pros:**
- Build on existing work
- Community support
- Proven functionality

**Cons:**
- May not support telnet
- Version compatibility issues
- 800 series support unknown

### Option 3: Hybrid Approach
**Pros:**
- Use pywattbox for HTTP devices
- Custom telnet client for 800 series
- Best of both worlds

**Cons:**
- More complex implementation
- Two different code paths

## Next Steps Recommendations

### Immediate Actions
1. **Test Current pywattbox**: Install and test with your 800 series device
2. **Examine Source Code**: Try to find the actual GitHub repositories
3. **Test Telnet Commands**: Connect directly to your device and test commands

### Development Strategy
1. **Start with Telnet**: Build custom telnet client based on companion module
2. **Test with Real Device**: Validate commands with actual Wattbox 800
3. **Create HACS Integration**: Build integration using our telnet client
4. **Consider pywattbox**: Evaluate if we can use it for HTTP devices

## Questions for User

1. **Do you have access to test the current pywattbox library with your 800 series?**
2. **Would you prefer to build a custom telnet client or try to extend existing libraries?**
3. **Are you planning to use other Wattbox models besides the 800 series?**
4. **Do you want to start with testing telnet commands directly with your device?**

## Resources

### Libraries
- [pywattbox on PyPI](https://pypi.org/project/pywattbox/)
- [pywattbox by gjbadros](https://github.com/gjbadros/pywattbox)
- [wattbox-api (Node.js)](https://www.npmjs.com/package/wattbox-api)

### References
- [eseglem/hass-wattbox](https://github.com/eseglem/hass-wattbox/) - Existing HA integration
- [bitfocus/companion-module-snapav-wattbox](https://github.com/bitfocus/companion-module-snapav-wattbox/) - Companion module

---

*Research completed on January 21, 2025*
