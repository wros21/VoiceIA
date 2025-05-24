# modules/chat_ai.py

import os
import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def chat_with_ai_stream(prompt, system_prompt="Eres un asistente útil y conciso."):
    """Consulta a Claude con un mensaje y devuelve la respuesta completa como texto."""
    try:
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=1024,
            temperature=0.7,
            system=system_prompt,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.content[0].text  # Devuelve el contenido completo
    except Exception as e:
        return f"Error al comunicarse con Claude: {str(e)}"
