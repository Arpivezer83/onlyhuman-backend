from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from openai import OpenAI
import os

# .env betöltése
load_dotenv()

# Inicializáljuk az új OpenAI klienst
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "OnlyHuman AI Backend aktív 🚀"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message", "")

    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful tutor."},
                {"role": "user", "content": user_input}
            ]
        )
        reply = completion.choices[0].message.content.strip()
        return jsonify({ "reply": reply })

    except Exception as e:
        print("🔥 Hiba a /chat endpointon:", e)
        return jsonify({ "error": str(e) }), 500


if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))  # Render ezt fogja átadni
    app.run(host='0.0.0.0', port=port)
