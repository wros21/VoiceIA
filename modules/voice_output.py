# modules/voice_output.py
import pyttsx3

engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Velocidad de habla
engine.setProperty('volume', 1.0)  # Volumen máximo


def speak_response(text):
    print(f"Asistente: {text}")
    engine.say(text)
    engine.runAndWait()
