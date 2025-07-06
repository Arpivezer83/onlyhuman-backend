import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import openai

load_dotenv()

app = Flask(__name__)
CORS(app)

# OpenAI API kulcs betöltése környezeti változóból
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/")
def home():
    return "Backend működik!"

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_message = data.get("message", "")

        if not user_message:
            return jsonify({"error": "Hiányzó üzenet"}), 400

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Segítőkész AI vagy."},
                {"role": "user", "content": user_message}
            ]
        )

        answer = response['choices'][0]['message']['content']
        return jsonify({"response": answer})

    except Exception as e:
        print(f"🔥 Hiba a /chat endpointon: {e}")
        return jsonify({"error": str(e)}), 500

# Ez a rész biztosítja, hogy Render használni tudja a dinamikus PORT-ot
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
