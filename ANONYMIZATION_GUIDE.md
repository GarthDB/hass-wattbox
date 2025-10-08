# Screenshot Anonymization Guide

## Quick Anonymization Methods

### Method 1: macOS Preview (Easiest)
1. **Open screenshot** in Preview
2. **Click the markup button** (pencil icon)
3. **Add text boxes** over sensitive data
4. **Type generic replacements** (e.g., "192.168.1.100", "STXXXXXXXXXXXXX")
5. **Save as new file**

### Method 2: ImageMagick (Command Line)
```bash
# Add text overlay to anonymize data
magick input.png -pointsize 16 -fill white -stroke black -strokewidth 1 \
  -annotate +100+50 "192.168.1.100" output.png

# Add rectangle to cover sensitive area
magick input.png -fill white -stroke black -draw "rectangle 100,50 300,80" output.png
```

### Method 3: Online Tools
- **Photopea.com** (free Photoshop alternative)
- **Canva.com** (easy text overlay)
- **Remove.bg** (background removal)

## Common Data to Anonymize

### IP Addresses
- **Replace with**: `192.168.1.100` or `10.0.0.100`
- **Example**: `192.168.1.45` → `192.168.1.100`

### Device Names/Hostnames
- **Replace with**: `wattbox-device` or `wattbox-800`
- **Example**: `ST20196431G842A` → `wattbox-device`

### Serial Numbers
- **Replace with**: `STXXXXXXXXXXXXX` format
- **Example**: `ST20196431G842A` → `STXXXXXXXXXXXXX`

### MAC Addresses
- **Replace with**: `XX:XX:XX:XX:XX:XX`
- **Example**: `00:11:22:33:44:55` → `XX:XX:XX:XX:XX:XX`

### Personal Information
- **Names**: Replace with `User` or `Admin`
- **Locations**: Replace with `Home` or `Office`
- **Email addresses**: Replace with `user@example.com`

## Batch Anonymization Script

```bash
#!/bin/bash
# Simple anonymization using ImageMagick

for file in *.png; do
    echo "Processing $file..."

    # Add generic text overlay
    magick "$file" -pointsize 14 -fill white -stroke black -strokewidth 1 \
        -annotate +50+30 "Wattbox Integration" \
        -annotate +50+50 "192.168.1.100" \
        -annotate +50+70 "wattbox-device" \
        "anonymized_$file"
done
```

## Quality Checklist

Before using screenshots for HACS submission:

- ✅ **No sensitive data visible**
- ✅ **Clear, readable text**
- ✅ **Good contrast and lighting**
- ✅ **Professional appearance**
- ✅ **Shows key functionality**
- ✅ **Consistent naming convention**

## Screenshot-Specific Anonymization

### Configuration Form Screenshots
- Anonymize IP addresses in form fields
- Replace device names with generic ones
- Keep form structure and UI elements

### Device Card Screenshots
- Anonymize device identifiers
- Replace hostnames with generic names
- Keep entity names and structure

### Entity Screenshots
- Anonymize any device-specific data
- Keep entity states and values generic
- Maintain UI layout and design

## Final Review

Before submitting to HACS:
1. **Double-check** all sensitive data is anonymized
2. **Verify** screenshots show key functionality
3. **Ensure** professional appearance
4. **Test** that screenshots load properly
5. **Confirm** naming convention is consistent
