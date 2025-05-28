from fileinput import filename
import os
import re
import platform
import subprocess

from modules.voice_input import listen_command
from modules.voice_output import speak_response
from modules.automation import abrir_aplicacion, cerrar_aplicacion, buscar_archivos
from modules.multimedia import handle_multimedia
from modules.weather import get_weather
from modules.chat_ai import chat_with_ai_stream
from modules.enviocorreo import enviar_correo
from modules.envio_mensaje import enviar_mensaje


def abrir_archivo(ruta):
    try:
        if platform.system().lower() == "windows":
            os.startfile(ruta)
        elif platform.system().lower() == "darwin":
            subprocess.call(["open", ruta])
        elif platform.system().lower() == "linux":
            subprocess.call(["xdg-open", ruta])
        else:
            return f"No compatible con {platform.system()}"
        return f"Archivo abierto: {ruta}"
    except Exception as e:
        return f"No se pudo abrir el archivo: {e}"

def interpretar_comando(comando):
    comando = comando.lower()

    if "abrir" in comando:
        app = comando.replace("abrir", "").strip()
        return abrir_aplicacion(app)
    
    elif "cerrar" in comando:
        app = comando.replace("cerrar", "").strip()
        return cerrar_aplicacion(app)

    elif "buscar archivo" in comando or "buscar archivos" in comando:
        nombre = None
        tipo = None
        fecha = None

        if "llamado" in comando:
            partes = comando.split("llamado")
            nombre = partes[1].strip().split()[0]

        if ".pdf" in comando or ".txt" in comando or ".docx" in comando:
            tipo = re.search(r"\.\w+", comando).group()

        if "202" in comando:
            fecha_match = re.search(r"\d{4}-\d{2}-\d{2}", comando)
            if fecha_match:
                fecha = fecha_match.group()

        resultados = buscar_archivos(".", nombre=filename)
        if resultados:
            return f"Encontré {len(resultados)} archivos."
        else:
            return "No encontré ningún archivo con esos criterios."
    
    else:
        return "Comando no reconocido."

def main():
    speak_response("Hola, soy Viernes. Di 'Hola Viernes' para comenzar.")

    while True:
        trigger = listen_command().lower()
        if "hola viernes" in trigger:
            speak_response("¿En qué te puedo ayudar hoy?")
            break

    while True:
        command = listen_command().lower()

        if not command:
            speak_response("No escuché ningún comando, intenta de nuevo.")
            continue

        if any(exit_word in command for exit_word in ["salir", "apágate", "cerrar programa"]):
            speak_response("Hasta luego, cerrando el sistema.")
            break

        elif "clima" in command:
            palabras = command.split()
            ciudad = "Ciudad de Guatemala"
            if "en" in palabras:
                index = palabras.index("en")
                ciudad = " ".join(palabras[index + 1:])
            resultado = get_weather(ciudad)
            speak_response(resultado)

        elif any(word in command for word in ["chrome", "navegador"]):
            resultado = abrir_aplicacion("chrome")
            speak_response(resultado)

        elif any(word in command for word in ["visual studio", "vs code", "code"]):
            resultado = abrir_aplicacion("visual studio")
            speak_response(resultado)

        elif "spotify" in command:
            resultado = abrir_aplicacion("spotify")
            speak_response(resultado)
       
        #Abrir la calculadora
        elif any(word in command for word in ["calculadora", "calcular"]):
            resultado = abrir_aplicacion("calculadora")
            speak_response(resultado)
        
        #Pausar Spotify
        elif any(word in command for word in ["pausa spotify", "pausar spotify"]):
            from modules.multimedia import pause_spotify_macos
            resultado = pause_spotify_macos()
            speak_response(resultado)

        #Abrir Spotify
        elif any(word in command for word in ["siguiente canción", "siguiente spotify", "next spotify"]):
            from modules.multimedia import next_track_spotify_macos
            resultado = next_track_spotify_macos()
            speak_response(resultado)
        
        #Abrir Netflix
        elif any(word in command for word in ["netflix", "películas", "series"]):
            resultado = abrir_aplicacion("netflix")
            speak_response(resultado)
        
        #Poner música en youtube
        elif any(word in command for word in ["youtube", "música", "musica", "pon música", "pon musica"]):
            resultado = handle_multimedia(command)
            speak_response(resultado)
        
        #Buscar en la IA
        elif any(word in command for word in ["consulta", "información", "ayúdame", "pregunta", "háblame de"]):
            speak_response("Consultando a la IA...")
            try:
                respuesta = chat_with_ai_stream(command)
                speak_response(respuesta)
            except Exception as e:
                speak_response(f"Hubo un error consultando a la IA: {str(e)}")
        
        #Buscar en Google
        elif "busca en google" in command or "buscar en google" in command:
            speak_response("¿Qué quieres que busque en Google?")
            query = listen_command()
            if query:
                import webbrowser
                url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
                webbrowser.open(url)
                speak_response(f"Buscando {query} en Google.")
            else:
                speak_response("No escuché tu búsqueda.")
        #Buscar archivos        
        elif any(word in command for word in ["buscar archivo", "busca archivo", "encuentra archivo"]):
            speak_response("¿Qué archivo deseas buscar?")
            file_name = listen_command()
            if file_name:
                resultados = buscar_archivos(".", nombre=file_name)
                if resultados:
                    speak_response(f"Encontré {len(resultados)} archivos.")
                    for resultado in resultados:
                        speak_response(resultado)
                else:
                    speak_response("No encontré ningún archivo con ese nombre.")
            else:
                speak_response("No escuché el nombre del archivo.")

        elif any(word in command for word in ["abrir archivo", "abre archivo"]):
            speak_response("¿Qué archivo deseas abrir?")
            file_name = listen_command()
            if file_name:
                resultado = abrir_archivo(file_name)
                speak_response(resultado)
            else:
                speak_response("No escuché el nombre del archivo.")
        #Enviar correo        
        elif any(word in command for word in ["manda un correo", "enviar un correo", "quiero enviar un correo"]):
            speak_response("¿Cuál es el correo del destinatario?")
            nombre_destinatario = listen_command().lower().replace(" ", "")
            destinatario = f"{nombre_destinatario}@gmail.com"

            speak_response("¿Cuál es el asunto del correo?")
            asunto = listen_command()

            speak_response("¿Cuál es el mensaje?")
            cuerpo = listen_command()

            resultado = enviar_correo(destinatario, asunto, cuerpo)
            speak_response(resultado)
            
       #Enviar mensaje por telegram
        elif any(word in command for word in ["manda un mensaje", "enviar un mensaje", "quiero enviar un mensaje"]):
            speak_response("¿Cuál es el numero de telefono?")
            numero_telefono = listen_command().lower().replace(" ", "")
            numero = f"+502{numero_telefono}"
            speak_response("¿Cuál es el mensaje?")
            mensaje = listen_command()
            resultado = enviar_mensaje(numero, mensaje)
            speak_response(resultado)
        else:
            speak_response("No entendí el comando. Intenta nuevamente.")
            # Para usar interpretar_comando, descomenta esta línea:
            # respuesta = interpretar_comando(command)
            # speak_response(respuesta)

if __name__ == "__main__":
    main()
