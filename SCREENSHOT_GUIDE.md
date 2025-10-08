# Screenshot Guide for HACS Submission

This guide will help you create professional screenshots of the Wattbox integration for your HACS submission.

## Installation Methods

### Method 1: Direct File Copy (Recommended)

1. **Set your Home Assistant config path**:
   ```bash
   export HA_CONFIG_PATH=/path/to/your/ha/config
   # Common locations:
   # - Docker: /config
   # - Home Assistant OS: /config
   # - Home Assistant Core: ~/.homeassistant
   # - Home Assistant Supervised: /usr/share/hassio/homeassistant
   ```

2. **Run the installation script**:
   ```bash
   ./install_to_ha.sh
   ```

3. **Restart Home Assistant**

### Method 2: Manual Copy

1. **Copy the integration files**:
   ```bash
   cp -r custom_components/wattbox /path/to/your/ha/config/custom_components/
   ```

2. **Restart Home Assistant**

## Screenshots to Take

### 1. Integration Discovery
- **Location**: Settings → Devices & Services → Add Integration
- **Action**: Search for "Wattbox"
- **Screenshot**: Show the integration appearing in search results

### 2. Configuration Flow
- **Location**: Wattbox configuration dialog
- **Screenshots needed**:
  - Initial configuration form (Host, Username, Password, Polling Interval)
  - Success message after configuration
  - Error handling (if testing without real device)

### 3. Device Card
- **Location**: Settings → Devices & Services → Wattbox
- **Screenshot**: Show the device card with all entities

### 4. Entity Cards
- **Location**: Overview dashboard
- **Screenshots needed**:
  - Switch entities (outlets, master power, auto reboot)
  - Sensor entities (voltage, current, power, firmware info)
  - Binary sensor entities (device status, power lost, etc.)

### 5. Entity Details
- **Location**: Click on individual entities
- **Screenshots needed**:
  - Switch entity details (showing on/off state)
  - Sensor entity details (showing current values)
  - Binary sensor entity details (showing status)

## Screenshot Tips

### Browser Settings
- **Use a clean browser window** (no bookmarks, minimal UI)
- **Set browser zoom to 100%** for consistent sizing
- **Use a standard resolution** (1920x1080 or similar)
- **Take screenshots in both light and dark themes** if possible

### Screenshot Tools
- **macOS**: Cmd+Shift+4 for area selection, Cmd+Shift+3 for full screen
- **Windows**: Snipping Tool or Win+Shift+S
- **Linux**: GNOME Screenshot or similar

### Image Requirements
- **Format**: PNG preferred
- **Size**: Reasonable resolution (not too large, not too small)
- **Quality**: Clear, readable text
- **Naming**: Use descriptive names like `wattbox-config-flow.png`

## Testing Without Real Device

If you don't have a Wattbox device, you can still take screenshots:

1. **Install the integration** using any IP address
2. **The integration will show connection errors** - this is expected
3. **You can still see**:
   - Configuration flow
   - Entity cards (even if they show "unavailable")
   - UI layout and design
   - Error handling

## Screenshot Checklist

- [ ] Integration appears in search results
- [ ] Configuration flow form
- [ ] Configuration success/error handling
- [ ] Device card in Devices & Services
- [ ] Switch entities on dashboard
- [ ] Sensor entities on dashboard
- [ ] Binary sensor entities on dashboard
- [ ] Individual entity details
- [ ] Both light and dark themes (if possible)

## File Organization

Create a `screenshots/` directory and organize your images:

```
screenshots/
├── config-flow/
│   ├── search-results.png
│   ├── configuration-form.png
│   └── success-message.png
├── device-card/
│   └── device-overview.png
├── entities/
│   ├── switches.png
│   ├── sensors.png
│   └── binary-sensors.png
└── details/
    ├── switch-details.png
    ├── sensor-details.png
    └── binary-sensor-details.png
```

## Next Steps

After taking screenshots:

1. **Review images** for clarity and completeness
2. **Add to README** or create a dedicated screenshots section
3. **Update HACS submission** with image references
4. **Consider creating a GIF** showing the configuration flow

## Troubleshooting

### Integration Not Appearing
- Check that files were copied correctly
- Verify Home Assistant was restarted
- Check logs for any errors

### Configuration Errors
- This is normal without a real device
- You can still take screenshots of the error handling
- Consider using a mock device for better screenshots

### Entity States
- Entities may show "unavailable" without a real device
- This is expected and acceptable for screenshots
- Focus on the UI layout and design
