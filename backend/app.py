from flask import Flask, render_template, request, jsonify
from assistant import extract_features_from_message, find_matching_products, get_event_style_advice, classify_intent


app = Flask(__name__)

@app.route("/")
def index():
    return render_template("home.html")

@app.route("/fashionBot")
def fashion_bot():
    return render_template("index.html")

@app.route("/virtual-try-on")
def virtual_try_on():
    return render_template("tryon.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_msg = request.form.get("message")
    print("🔹 User message:", user_msg)

    intent = classify_intent(user_msg)
    print("🧭 Intent:", intent)

    if intent == "product_recommendation":
        filters = extract_features_from_message(user_msg)
        if not filters:
            return jsonify({"response": "⚠️ Sorry, I couldn't understand your request."})

        results = find_matching_products(filters)
        if not results:
            return jsonify({"response": "❌ No matching products found."})

        response_html = ""
        for item in results:
            response_html += f"""
            <div style='margin-bottom:20px;'>
                <b>{item['name']}</b><br>
                Price: ₹{item['budget']}<br>
                Tags: {', '.join(item['tags'])}<br>
                <img src='/{item['image']}' width='160'><br>
            </div>
            """
        return jsonify({"response": response_html})

    elif intent == "style_advice":
        advice = get_event_style_advice(user_msg)
        if not advice:
            return jsonify({"response": "⚠️ Couldn't generate style advice."})
        
        advice_html = "<div style='margin-bottom:20px;'><b>👗 Event Style Advice</b><br>"
        advice_html += f"<b>Dress Code:</b> {advice.get('dress_code', '')}<br>"
        if advice.get("outfit_options"):
            advice_html += "<b>Outfit Options:</b><ul>"
            for opt in advice["outfit_options"]:
                advice_html += f"<li>{opt}</li>"
            advice_html += "</ul>"
        if advice.get("style_tips"):
            advice_html += "<b>Style Tips:</b><ul>"
            for tip in advice["style_tips"]:
                advice_html += f"<li>{tip}</li>"
            advice_html += "</ul>"
        advice_html += "</div>"

        return jsonify({"response": advice_html})

    else:
        return jsonify({"response": "🤖 I'm not sure what you're asking. Try again?"})

if __name__ == "__main__":
    app.run(debug=True)

