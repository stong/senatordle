#!/usr/bin/env python3
"""
Try to download missing senator portraits from alternative sources
"""
import json
import urllib.request
import os
from pathlib import Path

# Missing senators and their bioguide IDs
missing_senators = [
    ("B001319", "Katie Boyd Britt"),
    ("A000382", "Angela D. Alsobrooks"),
    ("S001232", "Tim Sheehy"),
    ("M001242", "Bernie Moreno"),
    ("M001243", "David McCormick"),
    ("J000312", "James C. Justice"),
    ("H001104", "Jon Husted"),
    ("M001244", "Ashley Moody")
]

output_dir = Path("senator_portraits")

# Try bioguide.congress.gov photo URLs
print("Attempting to download from bioguide.congress.gov...\n")

for bioguide_id, name in missing_senators:
    # Try the bioguide direct photo URL
    image_url = f"https://bioguide.congress.gov/bioguide/photo/{bioguide_id[0]}/{bioguide_id}.jpg"
    output_file = output_dir / f"{bioguide_id}.jpg"

    try:
        print(f"Downloading {name}...", end=" ")
        urllib.request.urlretrieve(image_url, output_file)
        print("✓")
    except Exception as e:
        print(f"✗ Failed: {e}")

print("\nChecking download results...")
total = 0
for bioguide_id, name in missing_senators:
    output_file = output_dir / f"{bioguide_id}.jpg"
    if output_file.exists():
        size = output_file.stat().st_size
        print(f"  ✓ {name}: {size:,} bytes")
        total += 1
    else:
        print(f"  ✗ {name}: Not found")

print(f"\nSuccessfully downloaded {total} additional portraits")
