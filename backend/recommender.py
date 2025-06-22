import json

with open("catalog/outfits.json", "r") as f:
    CATALOG = json.load(f)

def recommend_from_preferences(gender, bodytype, occasion, color, budget, style):
    matches = []

    for item in CATALOG:
        score = 0
        tags = item["tags"]

        # basic keyword scoring
        if gender.lower() in tags: score += 1
        if bodytype.lower() in tags: score += 1
        if occasion.lower() in tags: score += 1
        if color.lower() in tags: score += 1
        if style.lower() in tags: score += 1
        if item["budget"] <= int(budget): score += 1

        matches.append((score, item))

    matches.sort(reverse=True, key=lambda x: x[0])
    return [x[1] for x in matches[:3]]

import re

# Define helper keyword banks
COLORS = [
    "white", "black", "blue", "green", "red", "yellow", "pink", "grey", "brown", "purple", "orange", "beige", "navy", "pastel"
]
TYPES = [
    "jacket", "tshirt", "shirt", "shorts", "shoes", "sandals", "bag", "backpack", "top", "dress", "scarf", "necklace"
]
BODYTYPES = ["petite", "lean", "plus size", "curvy"]
OCCASIONS = ["beach", "party", "casual", "sports", "office", "wedding", "vacation", "gym"]
STYLES = ["boho", "chic", "casual", "sporty", "classy", "traditional", "minimal"]
GENDER= ["male","female"]
def extract_keywords_from_blurb(blurb):
    blurb = blurb.lower()
    keywords = set()

    for word in GENDER + COLORS + TYPES + BODYTYPES + OCCASIONS + STYLES:
        if word in blurb:
            keywords.add(word)

    return keywords

def recommend_from_groq_blurb(blurb):
    keywords = extract_keywords_from_blurb(blurb)
    matches = []

    for item in CATALOG:
        score = len(set(item["tags"]) & keywords)
        if score > 0:
            matches.append((score, item))

    matches.sort(reverse=True, key=lambda x: x[0])
    return [x[1] for x in matches[:5]]  # Top 5 matches

