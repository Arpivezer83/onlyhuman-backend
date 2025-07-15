from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

client = OpenAI()  # OpenAI kliens (kulcsot automatikusan beolvassa)

# Agent promptok

def math_agent_prompt(nickname, goal, level):
    return (
        f"Te egy kedves, türelmes AI matektanár vagy. "
        f"A tanuló neve: {nickname}, szintje: {level}, célja: {goal}. "
        f"Magyarázd el egyszerűen és érthetően a matekkal kapcsolatos kérdéseket."
    )

def speak_agent_prompt(nickname, goal, level):
    return (
        f"Te egy barátságos AI nyelvtanár vagy. "
        f"A tanuló neve: {nickname}, szintje: {level}, célja: {goal}. "
        f"Beszélgess vele angolul, javítsd ki kedvesen a hibákat, és bátorítsd őt a gyakorlásban."
    )

def coach_agent_prompt(nickname, goal, level):
    return (
        f"Te egy AI életvezetési coach vagy. "
        f"A tanuló neve: {nickname}, szintje: {level}, célja: {goal}. "
        f"Kérdezd meg a napi célját, adj motivációt, és segítsd a fejlődését."
    )

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        message = data.get("message", "")
        profile = data.get("profile", {})

        nickname = profile.get("nickname", "Tanuló")
        goal = profile.get("goal", "segíteni neki a tanulásban")
        level = profile.get("level", "ismeretlen")
        agent = profile.get("agent", "math")  # Default: matek

        # Agent kiválasztás
        if agent == "math":
            system_prompt = math_agent_prompt(nickname, goal, level)
        elif agent == "speak":
            system_prompt = speak_agent_prompt(nickname, goal, level)
        elif agent == "coach"
