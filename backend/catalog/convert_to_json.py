# backend/catalog/convert_to_json.py
import csv, json, os, random, pathlib

BASE_DIR   = pathlib.Path(__file__).resolve().parent.parent      # .../backend
CSV_PATH   = BASE_DIR / "catalog" / "styles.csv"
OUT_JSON   = BASE_DIR / "catalog" / "outfits.json"
IMG_DIR    = BASE_DIR / "static" / "outfits"

MAX_ITEMS  = 40   # how many products you want in the mini‑catalog

fields = ["id", "gender", "baseColour", "usage", "articleType",
          "productDisplayName"]

items = []
with open(CSV_PATH, newline='', encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        if not all(row[k] for k in fields):
            continue                         # skip rows with missing data

        img_file = IMG_DIR / f"{row['id']}.jpg"
        if not img_file.exists():
            continue                         # only keep rows with a local image

        items.append({
            "name": row["productDisplayName"].title(),
            "image": str(img_file.relative_to(BASE_DIR)),        # static/outfits/xxxxx.jpg
            "tags": [
                row["gender"].strip().lower(),
                row["baseColour"].strip().lower(),
                row["usage"].strip().lower(),
                row["articleType"].strip().lower()
            ],
            "budget": random.randint(1500, 4000)                 # dummy price
        })

        if len(items) >= MAX_ITEMS:
            break

with open(OUT_JSON, "w", encoding="utf-8") as f:
    json.dump(items, f, indent=2)

print(f"✅ Wrote {len(items)} items → {OUT_JSON.relative_to(BASE_DIR)}")
