from flask import Flask, render_template, request, jsonify
from assistant import extract_features_from_message, find_matching_products

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_msg = request.form.get("message")
    print("🔹 User message:", user_msg)
    filters = extract_features_from_message(user_msg)
    print("🧠 Extracted filters:", filters)
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

if __name__ == "__main__":
    app.run(debug=True)
