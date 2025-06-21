from flask import Flask,render_template, request, jsonify
from chatbot import generate_response
from recommender import recommend_from_preferences

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/recommend", methods=["POST"])
def recommend():
    # Get form input
    gender   = request.form.get("gender")
    occasion = request.form.get("occasion")
    budget   = request.form.get("budget")
    style    = request.form.get("style")
    color    = request.form.get("colour")
    bodytype = request.form.get("bodytype")

    # Use GPT to generate a friendly explanation
    prompt = f"Suggest an outfit under ₹{budget} for a {bodytype} {gender} going to a {occasion}. Style: {style}, prefers {color} colors."
    stylist_blurb = generate_response(prompt)

    # Run rule-based recommender
    top_items = recommend_from_preferences(gender, bodytype, occasion, color, budget, style)

    # Build outfit cards
    outfits = []
    for item in top_items:
        outfits.append({
            "img": item["image"],
            "title": item["name"]
        })

    return render_template("results.html", blurb=stylist_blurb, outfits=outfits, celeb_img=None)

if __name__ == "__main__":
    app.run(debug=True)
