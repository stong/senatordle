#!/usr/bin/env python3
"""
Download portraits of all current US Senators
"""
import json
import urllib.request
import os
from pathlib import Path

# Create output directory
output_dir = Path("senator_portraits")
output_dir.mkdir(exist_ok=True)

# Load legislators data
with open("legislators-current.json", "r") as f:
    legislators = json.load(f)

# Filter for current senators
senators = [leg for leg in legislators if leg.get("terms") and leg["terms"][-1]["type"] == "sen"]

print(f"Found {len(senators)} current senators")

# Download portraits
base_url = "https://unitedstates.github.io/images/congress/original"
downloaded = 0
failed = []

for senator in senators:
    bioguide_id = senator["id"]["bioguide"]
    name = senator["name"]["official_full"]
    state = senator["terms"][-1]["state"]
    party = senator["terms"][-1]["party"]

    # Download image
    image_url = f"{base_url}/{bioguide_id}.jpg"
    output_file = output_dir / f"{bioguide_id}.jpg"

    try:
        print(f"Downloading {name} ({party}-{state})...", end=" ")
        urllib.request.urlretrieve(image_url, output_file)
        downloaded += 1
        print("✓")
    except Exception as e:
        print(f"✗ Failed: {e}")
        failed.append({"name": name, "bioguide": bioguide_id, "error": str(e)})

print(f"\n{'='*60}")
print(f"Downloaded: {downloaded}/{len(senators)} portraits")

if failed:
    print(f"Failed: {len(failed)}")
    for f in failed:
        print(f"  - {f['name']} ({f['bioguide']}): {f['error']}")

# Save metadata
metadata = []
for senator in senators:
    bioguide_id = senator["id"]["bioguide"]
    metadata.append({
        "bioguide_id": bioguide_id,
        "name": senator["name"]["official_full"],
        "first_name": senator["name"].get("first", ""),
        "last_name": senator["name"].get("last", ""),
        "state": senator["terms"][-1]["state"],
        "party": senator["terms"][-1]["party"],
        "image_file": f"{bioguide_id}.jpg"
    })

with open(output_dir / "senators_metadata.json", "w") as f:
    json.dump(metadata, f, indent=2)

print(f"\nMetadata saved to senator_portraits/senators_metadata.json")
