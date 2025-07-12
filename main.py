from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        message = data.get("message", "")
        profile = data.get("profile", {})

        nickname = profile.get("nickname", "Tanuló")
        goal = profile.get("goal", "segíteni neki a tanulásban")
        level = profile.get("level", "ismeretlen")

        system_prompt = (
            f"Te egy kedves, türelmes AI matektanár vagy. "
            f"A tanuló neve: {nickname}, szintje: {level}, célja: {goal}. "
            f"Kérlek, szólítsd meg őt a nevén (pl. Szia {nickname}!) és figyelembe véve a szintjét ({level}) és célját ({goal}), segíts neki egyszerűen és érthetően."
        )

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message},
            ],
        )

        reply = completion.choices[0].message["content"]
        return jsonify({"reply": reply})

    except Exception as e:
        print("🔥 Hiba a /chat endpointon:", e)
        return jsonify({"error": "Hiba történt a válasz generálásakor."}), 500

if __name__ == "__main__":
    app.run(debug=False)
