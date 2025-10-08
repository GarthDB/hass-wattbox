#!/bin/bash

# Screenshot Renaming Script for HACS Submission
# This script helps rename screenshots with proper naming convention

echo "🔌 Wattbox Integration Screenshot Renaming"
echo "=========================================="
echo

# Create backup directory
echo "📁 Creating backup of original screenshots..."
mkdir -p screenshots_backup
cp screenshots/*.png screenshots_backup/
echo "✅ Backup created in screenshots_backup/"
echo

# Navigate to screenshots directory
cd screenshots

echo "📸 Current screenshots:"
ls -la *.png
echo

echo "🔄 Renaming screenshots..."
echo "Please review each screenshot and confirm the suggested name:"
echo

# Rename files with confirmation
echo "1. Renaming 'Screenshot 2025-10-08 at 5.07.22 PM.png' → '01-hacs-search-results.png'"
read -p "   Is this correct? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    mv "Screenshot 2025-10-08 at 5.07.22 PM.png" "01-hacs-search-results.png"
    echo "   ✅ Renamed"
else
    echo "   ⏭️  Skipped"
fi
echo

echo "2. Renaming 'Screenshot 2025-10-08 at 5.07.42 PM.png' → '02-configuration-form.png'"
read -p "   Is this correct? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    mv "Screenshot 2025-10-08 at 5.07.42 PM.png" "02-configuration-form.png"
    echo "   ✅ Renamed"
else
    echo "   ⏭️  Skipped"
fi
echo

echo "3. Renaming 'Screenshot 2025-10-08 at 5.07.56 PM.png' → '03-configuration-success.png'"
read -p "   Is this correct? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    mv "Screenshot 2025-10-08 at 5.07.56 PM.png" "03-configuration-success.png"
    echo "   ✅ Renamed"
else
    echo "   ⏭️  Skipped"
fi
echo

echo "4. Renaming 'Screenshot 2025-10-08 at 5.08.27 PM.png' → '04-device-card.png'"
read -p "   Is this correct? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    mv "Screenshot 2025-10-08 at 5.08.27 PM.png" "04-device-card.png"
    echo "   ✅ Renamed"
else
    echo "   ⏭️  Skipped"
fi
echo

echo "5. Renaming 'Screenshot 2025-10-08 at 5.08.45 PM.png' → '05-switch-entities.png'"
read -p "   Is this correct? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    mv "Screenshot 2025-10-08 at 5.08.45 PM.png" "05-switch-entities.png"
    echo "   ✅ Renamed"
else
    echo "   ⏭️  Skipped"
fi
echo

echo "6. Renaming 'Screenshot 2025-10-08 at 5.09.04 PM.png' → '06-sensor-entities.png'"
read -p "   Is this correct? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    mv "Screenshot 2025-10-08 at 5.09.04 PM.png" "06-sensor-entities.png"
    echo "   ✅ Renamed"
else
    echo "   ⏭️  Skipped"
fi
echo

echo "7. Renaming 'Screenshot 2025-10-08 at 5.09.14 PM.png' → '07-entity-details.png'"
read -p "   Is this correct? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    mv "Screenshot 2025-10-08 at 5.09.14 PM.png" "07-entity-details.png"
    echo "   ✅ Renamed"
else
    echo "   ⏭️  Skipped"
fi
echo

echo "📋 Final screenshot list:"
ls -la *.png
echo

echo "🎯 Next steps:"
echo "1. Review each renamed screenshot"
echo "2. Anonymize any sensitive data (IPs, serial numbers, etc.)"
echo "3. Choose the best 5-7 screenshots for HACS submission"
echo "4. Add screenshots to your README or documentation"
echo

echo "✅ Screenshot renaming complete!"
