import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

MISTRAL_API_KEY = "9JZcncIN9tSDXyA00KqX6f2GC7soAEW0"

@app.route("/")
def home():
    return "✅ MathGenius AI server ishlayapti!"

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question")

    if not question:
        return jsonify({"error": "❗Savol bo‘sh bo‘lishi mumkin emas"}), 400

    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "mistral-large-latest",
        "messages": [
            {
                "role": "system",
                "content": "Siz o‘zbek tilida gapiradigan sun’iy intellekt yordamchisiz. Javoblarni aniq va tushunarli bering."
            },
            {
                "role": "user",
                "content": question
            }
        ]
    }

    response = requests.post("https://api.mistral.ai/v1/chat/completions", headers=headers, json=payload)

    if response.status_code == 200:
        reply = response.json()["choices"][0]["message"]["content"]
        return jsonify({"answer": reply})
    else:
        return jsonify({"error": f"❌ Mistral API xatolik: {response.status_code}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render avtomatik PORT beradi
    app.run(host="0.0.0.0", port=port)
