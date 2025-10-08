# Screenshot Organization Guide for HACS Submission

## Current Screenshots (in chronological order)

1. **Screenshot 2025-10-08 at 5.07.22 PM.png** (918KB)
2. **Screenshot 2025-10-08 at 5.07.42 PM.png** (912KB)
3. **Screenshot 2025-10-08 at 5.07.56 PM.png** (924KB)
4. **Screenshot 2025-10-08 at 5.08.27 PM.png** (931KB)
5. **Screenshot 2025-10-08 at 5.08.45 PM.png** (935KB) - *This one shows the device name issue you mentioned*
6. **Screenshot 2025-10-08 at 5.09.04 PM.png** (932KB)
7. **Screenshot 2025-10-08 at 5.09.14 PM.png** (1.07MB)

## Recommended Naming Convention

Based on typical HACS submission flow, here's the suggested naming:

### Essential Screenshots for HACS:
1. **`01-hacs-search-results.png`** - Shows Wattbox appearing in HACS search
2. **`02-configuration-form.png`** - Configuration dialog with form fields
3. **`03-configuration-success.png`** - Success message after setup
4. **`04-device-card.png`** - Device card in Settings → Devices & Services
5. **`05-switch-entities.png`** - Switch entities on dashboard
6. **`06-sensor-entities.png`** - Sensor entities on dashboard
7. **`07-entity-details.png`** - Individual entity details view

## Anonymization Checklist

Before using screenshots, ensure you've anonymized:

### ✅ Data to Anonymize:
- **IP Addresses**: Replace with `192.168.1.100` or `10.0.0.100`
- **Device Names/Hostnames**: Replace with generic names like `wattbox-device`
- **Serial Numbers**: Replace with `STXXXXXXXXXXXXX` format
- **MAC Addresses**: Replace with `XX:XX:XX:XX:XX:XX`
- **Personal Information**: Remove any personal names, locations, etc.
- **Network Details**: Genericize network topology information
- **Device Identifiers**: Use generic device identifiers

### 🎨 Anonymization Tools:
- **macOS Preview**: Use markup tools to add text boxes over sensitive data
- **ImageMagick**: Command-line tool for batch processing
- **GIMP/Photoshop**: Professional image editing
- **Online Tools**: Various online image editors

## Step-by-Step Organization Process

### Step 1: Review Each Screenshot
Open each screenshot and identify:
- What UI element it shows
- What sensitive data needs anonymization
- Whether it's suitable for HACS submission

### Step 2: Anonymize Sensitive Data
For each screenshot that needs anonymization:
1. Open in your preferred image editor
2. Add text boxes or shapes over sensitive data
3. Replace with generic placeholder text
4. Save as a new file

### Step 3: Rename Files
Use the suggested naming convention above, keeping the most important screenshots.

### Step 4: Create Final Set
Choose the best 5-7 screenshots that show:
- Integration discovery
- Configuration process
- Device management
- Entity functionality
- User interface quality

## Quick Rename Commands

```bash
# Navigate to screenshots directory
cd screenshots

# Rename files (adjust based on what each screenshot shows)
mv "Screenshot 2025-10-08 at 5.07.22 PM.png" "01-hacs-search-results.png"
mv "Screenshot 2025-10-08 at 5.07.42 PM.png" "02-configuration-form.png"
mv "Screenshot 2025-10-08 at 5.07.56 PM.png" "03-configuration-success.png"
mv "Screenshot 2025-10-08 at 5.08.27 PM.png" "04-device-card.png"
mv "Screenshot 2025-10-08 at 5.08.45 PM.png" "05-switch-entities.png"
mv "Screenshot 2025-10-08 at 5.09.04 PM.png" "06-sensor-entities.png"
mv "Screenshot 2025-10-08 at 5.09.14 PM.png" "07-entity-details.png"
```

## HACS Submission Requirements

For HACS submission, you typically need:
- **3-5 high-quality screenshots** showing key functionality
- **Clean, professional appearance** with no sensitive data
- **Clear demonstration** of integration features
- **Good lighting/contrast** for readability

## Next Steps

1. **Review each screenshot** to identify content and sensitive data
2. **Anonymize sensitive information** using image editing tools
3. **Rename files** using the suggested convention
4. **Select the best 5-7 screenshots** for submission
5. **Add to README** or create a dedicated screenshots section
