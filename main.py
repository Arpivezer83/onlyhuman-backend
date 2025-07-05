from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "")
    try:
        response = client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=[
                { "role": "system", "content": "Te egy barátságos AI tanár vagy." },
                { "role": "user", "content": user_message }
            ]
        )
        reply = response.choices[0].message.content
        return jsonify({ "reply": reply })
    except Exception as e:
        return jsonify({ "error": str(e) }), 500

# Ez nagyon fontos!
if __name__ == "__main__":
    app.run(debug=True)
