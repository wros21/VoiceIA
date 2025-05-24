# modules/voice_input.py
import speech_recognition as sr

def listen_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Escuchando...")
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio, language="es-ES")
        print(f"Comando reconocido: {command}")
        return command.lower()
    except sr.UnknownValueError:
        print("No se entendió el audio.")
        return ""
    except sr.RequestError:
        print("Error al conectarse al servicio de reconocimiento de voz.")
        return ""
