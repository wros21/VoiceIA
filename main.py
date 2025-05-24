# main.py
from modules.voice_input import listen_command
from modules.voice_output import speak_response
from modules.automation import handle_automation
from modules.multimedia import handle_multimedia
from modules.weather import get_weather
from modules.chat_ai import get_ai_response


def main():
    speak_response("Hola, soy tu asistente. ¿En qué puedo ayudarte?")

    while True:
        command = listen_command()

        if "clima" in command:
            result = get_weather()
        elif "abrir" in command:
            result = handle_automation(command)
        elif "reproduce" in command:
            result = handle_multimedia(command)
        elif "chat" in command:
            result = get_ai_response(command)
        elif "salir" in command:
            speak_response("Hasta luego!")
            break
        else:
            result = "No entendí el comando."

        speak_response(result)


if __name__ == "__main__":
    main()
