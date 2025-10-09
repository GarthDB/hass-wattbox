# Wattbox Integration Development Continuation Guide

## Project Overview
This is a Home Assistant custom integration for SnapAV Wattbox power distribution units. The project is located at `/Users/garthdb/Projects/ha-wattbox/` and is being prepared for HACS submission.

## Current Status (as of 2025-10-08)

### Critical Issue: NoneType Errors
The integration is experiencing persistent `NoneType` errors during entity setup across all platforms (binary_sensor, sensor, switch). Despite extensive debugging, the root cause remains elusive.

### Key Findings from Diagnostic Logs
- **async_add_entities is NOT None**: Diagnostic logs show it's a valid bound method
- **All variables are valid**: coordinator, sensors, valid_sensors are all properly initialized
- **Error occurs inside async_add_entities call**: The NoneType error happens within Home Assistant's entity platform code
- **Home Assistant caching issue**: The system appears to be running cached versions of files despite updates

### Current Version
- **Latest Release**: v0.2.14 (FORCE RELOAD version)
- **Manifest Version**: 0.2.14
- **Status**: Complete file rewrite to break Home Assistant caching

## Project Structure
```
/Users/garthdb/Projects/ha-wattbox/
├── custom_components/wattbox/
│   ├── __init__.py
│   ├── binary_sensor.py          # v0.2.14 - FORCE RELOAD with extensive diagnostics
│   ├── config_flow.py
│   ├── const.py
│   ├── coordinator.py
│   ├── entity.py
│   ├── hacs.json
│   ├── icon.png, icon@2x.png
│   ├── logo.png, logo@2x.png
│   ├── manifest.json             # v0.2.14
│   ├── sensor.py
│   ├── switch.py
│   └── telnet_client.py
├── docs/
│   ├── HACS_INTEGRATION_GUIDE.md
│   ├── INTEGRATION_TEST_RESULTS.md
│   └── screenshots/              # Final anonymized screenshots
├── tests/
│   └── [test files]
├── README.md
└── [other project files]
```

## Recent Development History

### Phase 1: HACS Preparation (Completed)
- ✅ Created HACS-compatible structure
- ✅ Added branding assets (icon.png, logo.png, @2x versions)
- ✅ Created anonymized screenshots
- ✅ Updated documentation
- ✅ Established release process

### Phase 2: Device Naming Improvements (Completed)
- ✅ Enhanced config_flow.py to capture device info during setup
- ✅ Implemented user-friendly device naming (hostname, model)
- ✅ Fixed field assignment issues (serial/model/hostname swapping)

### Phase 3: Telnet Communication Fixes (Completed)
- ✅ Resolved telnet command sequencing issues
- ✅ Fixed decode errors with telnetlib3
- ✅ Implemented proper buffer management
- ✅ Added comprehensive error handling

### Phase 4: NoneType Error Debugging (In Progress)
- ❌ **BLOCKING ISSUE**: Persistent NoneType errors during entity setup
- 🔄 **Current Approach**: v0.2.14 FORCE RELOAD with extensive diagnostics

## Technical Details

### NoneType Error Pattern
```
Error while setting up wattbox platform for [binary_sensor/sensor/switch]:
object NoneType can't be used in 'await' expression
Traceback (most recent call last):
  File "/usr/src/homeassistant/homeassistant/helpers/entity_platform.py", line 451, in _async_setup_platform
    await asyncio.shield(awaitable)
  File "/config/custom_components/wattbox/[platform].py", line [X], in async_setup_entry
    await async_add_entities(valid_[entities])
TypeError: object NoneType can't be used in 'await' expression
```

### Diagnostic Logs Show
- ✅ `async_add_entities` is a valid bound method (NOT None)
- ✅ `coordinator` is properly initialized
- ✅ `sensors` list contains 5 valid sensor objects
- ✅ `valid_sensors` is a proper list with 5 entities
- ❌ **Error occurs inside the `async_add_entities` call itself**

### Home Assistant Caching Issue
The error traceback shows old line numbers that don't match the current file structure, indicating Home Assistant is running cached versions of the files despite:
- Multiple version bumps (0.2.10 → 0.2.14)
- Complete file rewrites
- Restarting Home Assistant
- Removing and re-adding the integration

## Next Steps for New Machine

### Immediate Actions
1. **Clone the repository**:
   ```bash
   git clone https://github.com/GarthDB/ha-wattbox.git
   cd ha-wattbox
   ```

2. **Check current status**:
   ```bash
   git status
   git log --oneline -10
   ```

3. **Run act tests** to verify current state:
   ```bash
   act -j test
   ```

### Debugging Strategy
The NoneType error is happening **inside** Home Assistant's `async_add_entities` call, not in our code. This suggests:

1. **Entity Object Issue**: One of the sensor/switch objects might have a None attribute that's being awaited
2. **Home Assistant Platform Issue**: There might be a compatibility issue with the current HA version
3. **Async Context Issue**: The entities might be created in the wrong async context

### Recommended Investigation Path
1. **Check Home Assistant Version**: Verify compatibility with the integration
2. **Examine Entity Classes**: Look for any async methods that might return None
3. **Test with Minimal Entities**: Create a version with only one entity to isolate the issue
4. **Check HA Logs**: Look for any additional error context in Home Assistant logs
5. **Test on Different HA Version**: Try on a different HA version to rule out compatibility issues

### Key Files to Focus On
- `custom_components/wattbox/binary_sensor.py` - Contains extensive diagnostic logging
- `custom_components/wattbox/entity.py` - Base entity class
- `custom_components/wattbox/coordinator.py` - Data coordinator
- Home Assistant logs during integration setup

### Testing Commands
```bash
# Run local tests
act -j test

# Check for linting issues
flake8 custom_components/wattbox/

# Format code
black custom_components/wattbox/
isort custom_components/wattbox/

# Run specific tests
python -m pytest tests/test_binary_sensor.py -v
```

## Environment Setup
- **Python**: 3.9+ (tested on 3.9, 3.10, 3.11, 3.12)
- **Dependencies**: See `requirements-test.txt`
- **Home Assistant**: 2023.1.0+ (as specified in hacs.json)
- **Testing**: Uses `act` CLI for GitHub Actions simulation

## Key Contacts
- **Repository**: https://github.com/GarthDB/ha-wattbox
- **Issues**: https://github.com/GarthDB/ha-wattbox/issues
- **HACS**: Ready for submission once NoneType errors are resolved

## Critical Notes
- The integration is functionally complete except for the NoneType errors
- All HACS requirements are met
- The issue appears to be a Home Assistant platform compatibility problem
- Extensive diagnostic logging is in place (v0.2.14) to help identify the root cause
- The error is NOT in our code but in how Home Assistant processes our entities

## Files Modified in Recent Debugging
- `custom_components/wattbox/binary_sensor.py` - Complete rewrite with diagnostics
- `custom_components/wattbox/sensor.py` - Added None checks
- `custom_components/wattbox/switch.py` - Added None checks
- `custom_components/wattbox/manifest.json` - Version 0.2.14

## Success Criteria
- [ ] NoneType errors eliminated
- [ ] All entities load successfully in Home Assistant
- [ ] Integration passes all act tests
- [ ] Ready for HACS submission
- [ ] Real device testing completed

---

**Last Updated**: 2025-10-08 23:30 MST
**Current Version**: v0.2.14
**Status**: Blocked on NoneType errors during entity setup
