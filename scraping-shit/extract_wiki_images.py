#!/usr/bin/env python3
"""
Extract senator image URLs from Wikipedia HTML
"""
from bs4 import BeautifulSoup
import json
import re

# Load the HTML
with open('senators_wiki.html', 'r') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

# Load existing metadata to match senators
with open('senator_portraits/senators_metadata.json', 'r') as f:
    senators_data = json.load(f)

print("Searching for senator images...")

# Find all img tags with senator portraits (those in upload.wikimedia.org and not SVG/seals)
all_images = soup.find_all('img')

senator_images = []

for img_tag in all_images:
    if 'src' not in img_tag.attrs:
        continue

    src = img_tag['src']

    # Filter for senator portraits
    if 'upload.wikimedia.org' not in src:
        continue
    if 'svg' in src.lower():
        continue
    if 'Seal' in src or 'seal' in src:
        continue
    if '/120px-' not in src:  # Senator portraits use this thumbnail size
        continue

    # Find the row containing this image
    row = img_tag.find_parent('tr')
    if not row:
        continue

    # Find name in the same row
    name_th = None
    for cell in row.find_all(['td', 'th']):
        if cell.name == 'th':
            span = cell.find('span', {'data-sort-value': True})
            if span:
                name_th = cell
                break

    if not name_th:
        continue

    # Extract name
    name_link = name_th.find('a')
    if not name_link:
        continue

    senator_name = name_link.text.strip()

    # Get image URL
    img_url = src
    if img_url.startswith('//'):
        img_url = 'https:' + img_url

    # Convert to higher resolution (320px instead of 120px)
    img_url = img_url.replace('/120px-', '/320px-')

    senator_images.append({
        'name': senator_name,
        'image_url': img_url
    })

print(f"Found {len(senator_images)} senators with images")

# Match with our bioguide data
matched = []
unmatched_bioguide = []

for senator in senators_data:
    found = False
    for wiki_senator in senator_images:
        # Match by last name
        if senator['last_name'].lower() in wiki_senator['name'].lower():
            matched.append({
                'bioguide_id': senator['bioguide_id'],
                'name': senator['name'],
                'wiki_name': wiki_senator['name'],
                'state': senator['state'],
                'party': senator['party'],
                'image_url': wiki_senator['image_url']
            })
            found = True
            break

    if not found:
        unmatched_bioguide.append(senator['name'])

print(f"Matched: {len(matched)}")

if unmatched_bioguide:
    print(f"Unmatched from bioguide: {len(unmatched_bioguide)}")
    if len(unmatched_bioguide) <= 20:
        for name in unmatched_bioguide:
            print(f"  - {name}")
    else:
        for name in unmatched_bioguide[:10]:
            print(f"  - {name}")
        print(f"  ... and {len(unmatched_bioguide) - 10} more")

# Save matched data
with open('wiki_image_urls.json', 'w') as f:
    json.dump(matched, f, indent=2)

print(f"\nSaved matched data to wiki_image_urls.json")
