# modules/weather.py
import requests
import os
from dotenv import load_dotenv
load_dotenv()

# Asegúrate de tener una clave válida de OpenWeatherMap en una variable de entorno llamada OWM_API_KEY
API_KEY = os.getenv("OWM_API_KEY")
CITY = "Ciudad de Guatemala"  # Puedes cambiar esta ciudad


def get_weather():
    if not API_KEY:
        return "No se encontró la clave API para el clima."

    url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&lang=es&units=metric"
    try:
        response = requests.get(url)
        data = response.json()

        if data.get("cod") != 200:
            return f"Error al obtener el clima: {data.get('message', 'desconocido')}"

        temp = data["main"]["temp"]
        description = data["weather"][0]["description"]
        return f"El clima en {CITY} es {description} con una temperatura de {temp}°C."

    except Exception as e:
        return f"Error al consultar el clima: {str(e)}"
