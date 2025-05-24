import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OWM_API_KEY")

def get_weather(city="Ciudad de Guatemala"):
    if not API_KEY:
        return "No se encontró la clave API para el clima."

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&lang=es&units=metric"
    try:
        respuesta = requests.get(url)
        data = respuesta.json()

        if data.get("cod") != 200:
            return f"No se pudo obtener el clima para {city}. Error: {data.get('message')}"

        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]
        humedad = data["main"]["humidity"]
        viento = data["wind"]["speed"]

        return (f"El clima en {city} es {desc} con una temperatura de {temp}°C, "
                f"humedad {humedad}% y viento a {viento} metros por segundo.")

    except Exception as e:
        return f"Error al consultar el clima: {e}"
