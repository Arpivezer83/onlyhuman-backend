from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

client = OpenAI()  # ÚJ KLIENS

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
            f"Te egy kedves, türelmes AI tanár vagy. "
            f"A tanuló neve: {nickname}, szintje: {level}, célja: {goal}. "
            f"Kérlek, szólítsd meg őt a nevén (pl. Szia {nickname}!), és figyelembe véve a szintjét és célját, "
            f"magyarázd el neki egyszerűen, érthetően a kérdéseit."
        )

        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message},
            ]
        )

        reply = completion.choices[0].message.content
        return jsonify({"reply": reply})

    except Exception as e:
        print("🔥 Hiba a /chat endpointon:", e)
        return jsonify({"error": "Hiba történt a válasz generálásakor."}), 500

if __name__ == "__main__":
    app.run(debug=False)
