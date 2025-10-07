# Companion Module Analysis - SnapAV Wattbox

## Overview
The [bitfocus/companion-module-snapav-wattbox](https://github.com/bitfocus/companion-module-snapav-wattbox) is a Node.js module for Bitfocus Companion that provides both HTTP and Telnet communication with Wattbox devices.

## Key Findings

### 1. Communication Protocols
- **Telnet**: Used for WB-250-IPW-2 (2 outlets) and custom models
- **HTTP**: Used for WB-300-IP-3, WB-700-IPV-12, WB-800VPS-IPVM-18
- **Port**: 23 for telnet, 80 for HTTP
- **Authentication**: Username/password based

### 2. Telnet Implementation Details

#### Connection Parameters
```javascript
const params = {
    host: self.config.ip,
    port: 23,
    loginPrompt: 'Username: ',
    passwordPrompt: 'Password: ',
    username: `${self.config.username}`,
    password: `${self.config.password}`,
    shellPrompt: 'Successfully Logged In!',
    timeout: 1500,
}
```

#### Key Telnet Commands
- `?Firmware` - Get firmware version
- `?Model` - Get device model
- `?ServiceTag` - Get serial number
- `?Hostname` - Get hostname
- `?OutletStatus` - Get all outlet states
- `~OutletStatus` - Get specific outlet state
- `?OutletName` - Get outlet names
- `?AutoReboot` - Get auto-reboot status
- `!OutletSet=<outlet>,<command>` - Control outlet
- `!Exit` - Disconnect

#### Command Structure
- **Query Commands**: Start with `?` (e.g., `?Firmware`)
- **Control Commands**: Start with `!` (e.g., `!OutletSet=1,ON`)
- **Response Format**: `command=value` (e.g., `?Firmware=2.4.1`)

### 3. Device Models Supported
```javascript
MODELS: [
    { id: '250', label: 'WB-250-IPW-2', protocol: 'telnet', outlets: 2 },
    { id: '300', label: 'WB-300-IP-3', protocol: 'http', outlets: 3 },
    { id: '300vb', label: 'WattBox WB-300VB-IP-5 300 Series IP Power Conditioner (VersaBox)', protocol: 'http', outlets: 5 },
    { id: '700', label: 'WB-700-IPV-12', protocol: 'http', outlets: 12 },
    { id: '800vps', label: 'WB-800VPS-IPVM-18', protocol: 'http', outlets: 18 },
    { id: 'other', label: 'Other' },
]
```

### 4. Data Structure
```javascript
DEVICE_DATA = {
    deviceInfo: {
        hostName: '',
        hardwareVersion: '',
        serialNumber: '',
        cloudStatus: 0,
        model: '',
        autoReboot: ''
    },
    powerInfo: {
        voltage: 0,
        current: 0,
        power: 0,
    },
    outletInfo: [
        { name: '', state: 0 }, // Array of outlet objects
    ],
}
```

### 5. Control Commands

#### Outlet Control
- **Power On**: `!OutletSet=<outlet>,ON`
- **Power Off**: `!OutletSet=<outlet>,OFF`
- **Power Cycle**: `!OutletSet=<outlet>,RESET` (via HTTP)
- **All Outlets**: Use outlet `0` for all outlets

#### Auto Reboot
- **Enable**: `!AutoReboot=ON`
- **Disable**: `!AutoReboot=OFF`

### 6. Response Processing
The module processes telnet responses by:
1. Splitting on `=` to separate command and value
2. Parsing comma-separated values for outlet data
3. Updating internal data structure
4. Triggering variable and feedback updates

### 7. Error Handling
- **API Locked**: Detects "API locked" message and stops polling
- **Connection Errors**: Logs errors and retries connection
- **Invalid Prompts**: Retries connection after 10 seconds
- **Queue Management**: Commands are queued and processed sequentially

## Key Insights for HACS Integration

### 1. Telnet is the Right Choice
- The companion module shows telnet is actively used and well-supported
- Command structure is simple and reliable
- Good error handling and connection management

### 2. Command Patterns
- Query commands use `?` prefix
- Control commands use `!` prefix
- Responses are in `command=value` format
- Outlet states are comma-separated values

### 3. Data Management
- Maintain device state in structured data object
- Process responses to update state
- Use polling for real-time updates
- Queue commands to avoid conflicts

### 4. Error Handling
- Handle "API locked" condition
- Implement connection retry logic
- Validate responses before processing
- Log errors for debugging

### 5. Configuration
- Support IP address, username, password
- Allow model selection or custom outlet count
- Enable/disable polling with configurable interval
- Verbose logging option

## Implementation Strategy for HACS

### Phase 1: Basic Telnet Client
1. Implement telnet connection using Python's `telnetlib`
2. Add authentication and connection management
3. Implement basic command sending and response parsing
4. Test with actual Wattbox 800 device

### Phase 2: Home Assistant Integration
1. Create configuration flow for setup
2. Implement sensor entities for device info and power data
3. Implement switch entities for outlet control
4. Add binary sensors for status indicators

### Phase 3: Advanced Features
1. Add polling for real-time updates
2. Implement error handling and reconnection
3. Add support for outlet naming
4. Add auto-reboot control

### Phase 4: Polish and Submission
1. Add comprehensive error handling
2. Write documentation and examples
3. Test with multiple Wattbox models
4. Submit to HACS

## Next Steps

1. **Test Telnet Commands**: Connect to actual Wattbox 800 and test the commands
2. **Create Python Telnet Client**: Implement basic telnet communication
3. **Generate HACS Structure**: Use cookiecutter to create integration template
4. **Implement Core Entities**: Create sensors and switches based on companion module patterns

---

*Analysis completed on January 21, 2025*
