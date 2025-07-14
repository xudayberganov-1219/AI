from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # ⚠️ Shart CORS-ni to‘g‘ri sozlash

MISTRAL_API_KEY = "9JZcncIN9tSDXyA00KqX6f2GC7soAEW0"

@app.route('/')
def home():
    return "✅ MathGenius AI server ishlayapti!"

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    question = data.get("question")

    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "mistral-large-latest",
        "messages": [
            {
                "role": "system",
                "content": "Siz tajribali o‘zbek tilida gapiradigan sun’iy intellekt yordamchisiz. Savollarga tushunarli va aniq qilib javob bering. Kerak bo‘lsa matematik formulalarni tushuntiring."
            },
            {
                "role": "user",
                "content": question
            }
        ]
    }

    response = requests.post("https://api.mistral.ai/v1/chat/completions", headers=headers, json=payload)

    if response.status_code == 200:
        result = response.json()
        reply = result["choices"][0]["message"]["content"]
        return jsonify({"answer": reply})
    else:
        return jsonify({"error": f"❌ Xatolik: {response.status_code}"}), 500

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=10000)  # Render uchun port majburan berilgan bo'lishi mumkin
