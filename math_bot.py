from flask import Flask, request, jsonify
import requests
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

MISTRAL_API_KEY = os.environ.get("MISTRAL_API_KEY")

@app.route('/')
def home():
    return '✅ MathGenius AI server ishlayapti!'

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
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
