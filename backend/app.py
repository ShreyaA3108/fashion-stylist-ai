from flask import Flask,render_template, request, jsonify
from chatbot import generate_response
from recommender import recommend_from_preferences,recommend_from_groq_blurb

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/recommend", methods=["POST"])
def recommend():
    # Get form input
    # gender   = request.form.get("gender")
    # occasion = request.form.get("occasion")
    # budget   = request.form.get("budget")
    # style    = request.form.get("style")
    # color    = request.form.get("colour")
    # bodytype = request.form.get("bodytype")

    # # Use GPT to generate a friendly explanation
    # # prompt = f"Suggest an outfit under ₹{budget} for a {bodytype} {gender} going to a {occasion}. Style: {style}, prefers {color} colors."
    # prompt = f"Suggest a one-line friendly fashion recommendation under ₹{budget} for a {bodytype} {gender} going to a {occasion}. Style: {style}. Prefers {color} colors. Keep it short. Do not list products. Do not include pricing or brand names."
    # stylist_blurb = generate_response(prompt)

    # # Run rule-based recommender
    # top_items = recommend_from_preferences(gender, bodytype, occasion, color, budget, style)

    # # Build outfit cards
    # outfits = []
    # for item in top_items:
    #     outfits.append({
    #         "img": item["image"],
    #         "title": item["name"]
    #     })

    # return render_template("result.html", blurb=stylist_blurb, outfits=outfits, celeb_img=None)
    gender   = request.form.get("gender")
    occasion = request.form.get("occasion")
    budget   = request.form.get("budget")
    style    = request.form.get("style")
    color    = request.form.get("colour")
    bodytype = request.form.get("bodytype")

    # GPT prompt
    prompt = f"Suggest a one-line friendly fashion recommendation under ₹{budget} for a {bodytype} {gender} going to a {occasion}. Style: {style}. Prefers {color} colors. Keep it short. Do not list products. Do not include pricing or brand names."
    stylist_blurb = generate_response(prompt)

    # Match from Groq output
    # Merge blurb with user inputs
    combined_text = f"{stylist_blurb}. Gender: {gender}, Bodytype: {bodytype}, Occasion: {occasion}, Style: {style}, Color: {color}"

    top_items = recommend_from_groq_blurb(combined_text)


    # Build outfit cards
    outfits = []
    for item in top_items:
        outfits.append({
            "img": item["image"].replace("static/", ""),  # ensure clean image path
            "title": item["name"]
        })

    return render_template("result.html", blurb=stylist_blurb, outfits=outfits, celeb_img=None)

if __name__ == "__main__":
    app.run(debug=True)
