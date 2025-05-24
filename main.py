from modules.voice_input import listen_command
from modules.voice_output import speak_response
from modules.automation import handle_automation, abrir_aplicacion
from modules.multimedia import handle_multimedia
from modules.weather import get_weather
from modules.chat_ai import chat_with_ai_stream

def main():
    speak_response("Hola, soy Viernes, tu asistente personal. ¿En qué puedo ayudarte?")

    while True:
        command = listen_command()
        if not command:
            speak_response("No escuché ningún comando, intenta de nuevo.")
            continue

        command = command.lower()

        # Procesamos solo si el comando empieza con "viernes"
        if not command.startswith("viernes"):
            continue

        # Quitamos la palabra clave para procesar solo el comando
        command = command.replace("viernes", "", 1).strip()

        if command in ["salir", "cerrar", "terminar", "adiós", "adios", "cierra"]:
            speak_response("Hasta luego!")
            break

        if "clima" in command:
            palabras = command.split()
            ciudad = "Ciudad de Guatemala"  # Por defecto
            if "en" in palabras:
                index = palabras.index("en")
                ciudad = " ".join(palabras[index + 1:])
            resultado = get_weather(ciudad)
            speak_response(resultado)

        elif any(word in command for word in ["chrome", "navegador"]):
            abrir_aplicacion("chrome")

        elif any(word in command for word in ["visual studio", "vs code", "code"]):
            abrir_aplicacion("code")

        elif "spotify" in command:
            abrir_aplicacion("spotify")

        elif "abrir" in command:
            resultado = handle_automation(command)
            speak_response(resultado)

        elif "reproduce" in command:
            resultado = handle_multimedia(command)
            speak_response(resultado)

        elif "chat" in command:
            speak_response("Consultando a la IA...")
            for chunk in chat_with_ai_stream(command):
                speak_response(chunk)

        else:
            speak_response("No entendí el comando.")

if __name__ == "__main__":
    main()
