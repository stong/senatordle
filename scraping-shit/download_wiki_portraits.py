#!/usr/bin/env python3
"""
Download senator portraits from Wikipedia URLs
"""
import json
import urllib.request
from pathlib import Path

# Load the matched data
with open('wiki_image_urls.json', 'r') as f:
    senators = json.load(f)

# Create output directory
output_dir = Path("wikipedia_portraits")
output_dir.mkdir(exist_ok=True)

print(f"Downloading {len(senators)} senator portraits from Wikipedia...")

downloaded = 0
failed = []

for senator in senators:
    bioguide_id = senator['bioguide_id']
    name = senator['name']
    image_url = senator['image_url']
    output_file = output_dir / f"{bioguide_id}.jpg"

    try:
        print(f"Downloading {name}...", end=" ")

        # Create request with user agent
        req = urllib.request.Request(
            image_url,
            headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'}
        )

        with urllib.request.urlopen(req) as response:
            with open(output_file, 'wb') as out_file:
                out_file.write(response.read())

        downloaded += 1
        print("✓")
    except Exception as e:
        print(f"✗ Failed: {e}")
        failed.append({'name': name, 'bioguide': bioguide_id, 'error': str(e)})

print(f"\n{'='*60}")
print(f"Downloaded: {downloaded}/{len(senators)} portraits")

if failed:
    print(f"Failed: {len(failed)}")
    for f in failed[:10]:
        print(f"  - {f['name']} ({f['bioguide']}): {f['error']}")
    if len(failed) > 10:
        print(f"  ... and {len(failed) - 10} more")
else:
    print("All portraits downloaded successfully!")
