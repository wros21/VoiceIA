# modules/chat_ai.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")


def get_ai_response(prompt):
    if not DEEPSEEK_API_KEY:
        return "No se encontró la clave API de DeepSeek."

    url = "https://api.deepseek.com/v1/chat/completions"  # Cambiar si la URL oficial es distinta
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "deepseek-chat",  # Cambiar según documentación oficial
        "messages": [
            {"role": "system", "content": "Eres un asistente útil y amable."},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"Error al consultar DeepSeek: {str(e)}"
