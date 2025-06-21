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
