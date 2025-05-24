# modules/chat_ai.py

import os
import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def chat_with_ai_stream(prompt, system_prompt="Eres un asistente útil y conciso."):
    """Consulta a Claude con un mensaje y devuelve la respuesta en tiempo real."""
    try:
        response = client.messages.create(
            model="claude-3-opus-20240229",  # O ajusta a 'claude-3-haiku-20240307' según tu suscripción
            max_tokens=300,
            temperature=0.7,
            system=system_prompt,
            messages=[
                {"role": "user", "content": prompt}
            ],
            stream=True
        )
        for chunk in response:
            yield chunk.content[0].text
    except Exception as e:
        yield f"Error al comunicarse con Claude: {str(e)}"