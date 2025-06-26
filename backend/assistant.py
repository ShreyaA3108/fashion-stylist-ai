import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
import re

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

with open("catalog/outfits.json", "r") as f:
    products = json.load(f)

def extract_features_from_message(message):
    prompt = f"""
You are a smart product assistant. Extract product preferences from this query:
"{message}"

Only output raw JSON. Respond with keys: gender, color, product_type, style, budget.
If any info is missing, set its value to null.

Example:
{{
  "gender": "men",
  "color": "black",
  "product_type": "tshirt",
  "style": "casual",
  "budget": 2500
}}
"""

    response = model.generate_content(prompt)
    raw = response.text.strip()
    print("🧠 Raw Gemini Response:\n", raw)

    # Remove markdown code blocks if present
    raw = raw.strip("`")  
    raw = re.sub(r"^json", "", raw, flags=re.IGNORECASE).strip()

    # Try to extract JSON object from messy text
    match = re.search(r"\{.*?\}", raw, re.DOTALL)
    if match:
        try:
            json_str = match.group()
            data = json.loads(json_str)

            # Ensure budget is an integer
            if data.get("budget") and isinstance(data["budget"], str):
                data["budget"] = int(re.sub(r"[^\d]", "", data["budget"]))

            return data
        except Exception as e:
            print("❌ JSON parsing failed:", e)
            return None
    else:
        print("❌ No JSON object found.")
        return None



def get_event_style_advice(user_intent):
    """
    Given a user intent (e.g., 'I'm going to a wedding next week in Jaipur'),
    return a dict with suggested dress code, outfit options, and style tips.
    """
    prompt = f"""
You are a fashion stylist assistant. A user says: "{user_intent}"

1. Suggest an appropriate dress code for the event and location.
2. Suggest 2-3 specific outfit options (describe the outfit, not brands).
3. Give 2-3 style tips (e.g., fabric, color, accessories) relevant to the event and location.

Respond in this JSON format:
{{
  "dress_code": "...",
  "outfit_options": [
    "...",
    "..."
  ],
  "style_tips": [
    "...",
    "..."
  ]
}}
"""
    response = model.generate_content(prompt)
    raw = response.text.strip()
    print("🧠 Event Style Advice Raw Response:\n", raw)

    # Remove markdown/code block formatting if present
    raw = raw.strip("`")
    raw = re.sub(r"^json", "", raw, flags=re.IGNORECASE).strip()

    # Try to extract JSON object from messy text
    match = re.search(r"\{.*?\}", raw, re.DOTALL)
    if match:
        try:
            json_str = match.group()
            data = json.loads(json_str)
            return data
        except Exception as e:
            print("❌ JSON parsing failed (event style advice):", e)
            return None
    else:
        print("❌ No JSON object found (event style advice).")
        return None


def find_matching_products(filters):
    matches = []

    for product in products:
        tags = [tag.lower() for tag in product["tags"]]
        score = 0

        def matches_any(value):
            return value and any(value.lower() in tag for tag in tags)

        # Gender and product_type are required
        if not matches_any(filters.get("gender")) or not matches_any(filters.get("product_type")):
            continue

        # Optional scoring
        if matches_any(filters.get("color")):
            score += 1
        if matches_any(filters.get("style")):
            score += 1
        if filters.get("budget"):
            try:
                if product["budget"] <= int(filters["budget"]):
                    score += 1
            except:
                pass

        # Always append, even with 0 score
        matches.append((product, score))

    # Sort matches by score (higher is better)
    matches.sort(key=lambda x: x[1], reverse=True)

    # Return only product dicts, top 5
    return [match[0] for match in matches[:5]]

def classify_intent(user_message):
    prompt = f"""
You are a classifier. A user says: "{user_message}"

Classify the intent as either:
- "product_recommendation"
- "style_advice"

Only return a JSON like: {{"intent": "..."}}. No explanation.
"""

    response = model.generate_content(prompt)
    raw = response.text.strip()

    raw = raw.strip("`")
    raw = re.sub(r"^json", "", raw, flags=re.IGNORECASE).strip()

    match = re.search(r"\{.*?\}", raw, re.DOTALL)
    if match:
        try:
            json_str = match.group()
            data = json.loads(json_str)
            return data.get("intent")
        except Exception as e:
            print("❌ Intent JSON parse failed:", e)
            return None
    return None

