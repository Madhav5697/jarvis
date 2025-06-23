import requests
import os
from dotenv import load_dotenv

# ✅ Load API key from .env.local
load_dotenv(dotenv_path=".env.local")
API_KEY = os.getenv("OPENROUTER_API_KEY")

def call_api(prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are J.A.R.V.I.S., a personal AI assistant created by Madhav — "
                    "sharp, sarcastic, and brutally honest. Speak with confidence, wit, and a calm tone. "
                    "Always refer to the user as 'sir'. Never act robotic. Your replies should feel cinematic, "
                    "efficient, and occasionally humorous, just like a normal user would’ve wanted."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=body
        )
        data = response.json()
        return data['choices'][0]['message']['content'].strip()

    except Exception as e:
        print(f"⚠️ API Error: {e}")
        return "Apologies sir, but I couldn't reach the AI server at the moment."
