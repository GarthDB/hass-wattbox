#!/usr/bin/env python3
"""
Screenshot Organization Script for HACS Submission

This script helps organize and rename screenshots for the Wattbox HACS submission.
It provides a systematic way to review each screenshot and assign appropriate names.
"""

import os
import shutil
from pathlib import Path

def organize_screenshots():
    """Organize screenshots with proper naming and anonymization guidance."""

    screenshots_dir = Path("screenshots")
    organized_dir = Path("screenshots_organized")

    # Create organized directory structure
    organized_dir.mkdir(exist_ok=True)
    (organized_dir / "config-flow").mkdir(exist_ok=True)
    (organized_dir / "device-card").mkdir(exist_ok=True)
    (organized_dir / "entities").mkdir(exist_ok=True)
    (organized_dir / "details").mkdir(exist_ok=True)

    # Screenshot files (in chronological order)
    screenshots = [
        "Screenshot 2025-10-08 at 5.07.22 PM.png",
        "Screenshot 2025-10-08 at 5.07.42 PM.png",
        "Screenshot 2025-10-08 at 5.07.56 PM.png",
        "Screenshot 2025-10-08 at 5.08.27 PM.png",
        "Screenshot 2025-10-08 at 5.08.45 PM.png",
        "Screenshot 2025-10-08 at 5.09.04 PM.png",
        "Screenshot 2025-10-08 at 5.09.14 PM.png"
    ]

    # Suggested naming convention based on typical HACS submission flow
    suggested_names = [
        "01-hacs-search-results.png",           # Integration search in HACS
        "02-configuration-form.png",            # Configuration form
        "03-configuration-success.png",         # Success message
        "04-device-card.png",                   # Device card in Devices & Services
        "05-switch-entities.png",               # Switch entities on dashboard
        "06-sensor-entities.png",               # Sensor entities on dashboard
        "07-entity-details.png"                 # Individual entity details
    ]

    print("🔌 Wattbox Integration Screenshot Organization")
    print("=" * 50)
    print()

    for i, (original, suggested) in enumerate(zip(screenshots, suggested_names), 1):
        print(f"📸 Screenshot {i}: {original}")
        print(f"   Suggested name: {suggested}")
        print(f"   Please review this screenshot and confirm:")
        print(f"   - What does it show?")
        print(f"   - Does the suggested name match?")
        print(f"   - Any sensitive data to anonymize?")
        print()

        # Copy to organized directory with suggested name
        src = screenshots_dir / original
        dst = organized_dir / suggested
        if src.exists():
            shutil.copy2(src, dst)
            print(f"   ✅ Copied to: {dst}")
        else:
            print(f"   ❌ Source file not found: {src}")
        print()

    print("📋 Anonymization Checklist:")
    print("-" * 30)
    print("✅ IP addresses (replace with 192.168.1.100)")
    print("✅ Device names/hostnames (replace with generic names)")
    print("✅ Serial numbers (replace with STXXXXXXXXXXXXX)")
    print("✅ MAC addresses (replace with XX:XX:XX:XX:XX:XX)")
    print("✅ Personal information")
    print("✅ Network topology details")
    print()

    print("🎯 Recommended Screenshots for HACS:")
    print("-" * 40)
    print("1. HACS search results showing 'Wattbox'")
    print("2. Configuration form (with anonymized data)")
    print("3. Success message after configuration")
    print("4. Device card in Devices & Services")
    print("5. Switch entities on dashboard")
    print("6. Sensor entities on dashboard")
    print("7. Individual entity details")
    print()

    print(f"📁 Organized screenshots saved to: {organized_dir}")
    print("Review each screenshot and rename as needed!")

if __name__ == "__main__":
    organize_screenshots()
