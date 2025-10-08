# HACS Installation Guide for Remote Home Assistant

Since your Home Assistant is on a separate machine (Home Assistant Yellow), here are the best ways to install and test the Wattbox integration:

## Method 1: HACS Custom Repository (Recommended)

This is the easiest method if you have HACS installed:

### Step 1: Push to GitHub
```bash
# Make sure your changes are committed and pushed
git add .
git commit -m "Prepare for HACS testing"
git push origin 9-hacs-submission
```

### Step 2: Add as Custom Repository in HACS
1. **Open Home Assistant** in your web browser
2. **Go to HACS** → Integrations
3. **Click the three dots menu** (⋮) in the top right
4. **Select "Custom repositories"**
5. **Add repository**:
   - **Repository**: `GarthDB/ha-wattbox`
   - **Category**: Integration
   - **Click "Add"**

### Step 3: Install the Integration
1. **Search for "Wattbox"** in HACS
2. **Click "Install"**
3. **Restart Home Assistant**

### Step 4: Configure the Integration
1. **Go to Settings** → Devices & Services
2. **Click "Add Integration"**
3. **Search for "Wattbox"**
4. **Enter your device details**

## Method 2: SSH/SCP Transfer

If you prefer direct file transfer:

### Step 1: Enable SSH on Home Assistant
1. **Go to Settings** → Add-ons → Add-on Store
2. **Search for "SSH & Web Terminal"**
3. **Install and configure it**
4. **Note the SSH credentials**

### Step 2: Set Environment Variables
```bash
export HA_HOST=your-ha-ip-address
export HA_USER=homeassistant
export HA_PORT=22  # Default SSH port
```

### Step 3: Run Installation Script
```bash
./install_to_remote_ha.sh
```

## Method 3: Manual File Transfer

### Step 1: Create a ZIP file
```bash
# Create a zip file of the integration
cd custom_components
zip -r wattbox.zip wattbox/
```

### Step 2: Transfer via Web Interface
1. **Access Home Assistant** via web browser
2. **Go to Settings** → Add-ons → SSH & Web Terminal
3. **Open the terminal**
4. **Upload the zip file** or use SCP to transfer it
5. **Extract and copy** the files to `/config/custom_components/`

## Screenshot Taking

Once installed, you can take screenshots by:

### Browser-Based Screenshots
1. **Access Home Assistant** via web browser
2. **Use browser developer tools** (F12) for clean screenshots
3. **Follow the screenshot guide** in `SCREENSHOT_GUIDE.md`

### Mobile App Screenshots
1. **Use the Home Assistant mobile app**
2. **Take screenshots** of the integration in action
3. **These often look more professional** for HACS submissions

## Testing Without Real Device

Even without a Wattbox device, you can:

1. **Install the integration** using any IP address
2. **Take screenshots** of the configuration flow
3. **See the entity cards** (they'll show "unavailable" but the UI will be visible)
4. **Test error handling** and UI responsiveness

## Troubleshooting

### Integration Not Appearing
- **Check HACS logs** for any errors
- **Verify the repository** was added correctly
- **Restart Home Assistant** after installation

### SSH Connection Issues
- **Verify SSH is enabled** on Home Assistant
- **Check firewall settings** on your network
- **Use the correct username** (usually "homeassistant")

### Configuration Errors
- **This is normal** without a real Wattbox device
- **Focus on UI screenshots** rather than functionality
- **Show error handling** in your screenshots

## Next Steps

After installation:

1. **Take comprehensive screenshots** following the guide
2. **Test the configuration flow** thoroughly
3. **Document any issues** you encounter
4. **Prepare for HACS submission** with all required materials

## File Structure After Installation

Your Home Assistant should have:
```
/config/custom_components/wattbox/
├── __init__.py
├── binary_sensor.py
├── config_flow.py
├── const.py
├── coordinator.py
├── entity.py
├── hacs.json
├── icon.png
├── icon@2x.png
├── logo.png
├── logo@2x.png
├── manifest.json
├── sensor.py
├── switch.py
└── telnet_client.py
```
