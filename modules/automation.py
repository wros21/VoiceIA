import subprocess
import platform
import os
import webbrowser
import re
import datetime

def abrir_aplicacion(nombre):
    sistema = platform.system().lower()

    if "netflix" in nombre.lower():
        webbrowser.open("https://www.netflix.com")
        return "Abriendo Netflix en el navegador."
    
    apps_mac = {
        "chrome": "Google Chrome",
        "code": "Visual Studio Code",
        "visual studio": "Visual Studio Code",
        "spotify": "Spotify"
    }

    try:
        if sistema == "darwin":  # macOS
            app_name = apps_mac.get(nombre.lower(), nombre)
            app_path = f"/Applications/{app_name}.app"
            if not os.path.exists(app_path):
                return f"La aplicación {app_name} no está instalada en este sistema."

            subprocess.Popen(["open", "-a", app_name])
            return f"Abriendo {app_name}"

        elif sistema == "windows":
            subprocess.Popen(f"start {nombre}", shell=True)
            return f"Abriendo {nombre.capitalize()}"

        elif sistema == "linux":
            subprocess.Popen([nombre])
            return f"Abriendo {nombre.capitalize()}"

        else:
            return f"Sistema operativo no compatible: {sistema}"

    except Exception as e:
        return f"No pude abrir {nombre}: {str(e)}"

def cerrar_aplicacion(nombre):
    sistema = platform.system().lower()

    apps_mac = {
        "chrome": "Google Chrome",
        "code": "Visual Studio Code",
        "visual studio": "Visual Studio Code",
        "spotify": "Spotify"
    }

    try:
        if sistema == "darwin":  # macOS
            app_name = apps_mac.get(nombre.lower(), nombre)
            app_path = f"/Applications/{app_name}.app"
            if not os.path.exists(app_path):
                return f"La aplicación {app_name} no está instalada en este sistema."

            subprocess.Popen(["osascript", "-e", f'tell application "{app_name}" to quit'])
            return f"Cerrando {app_name}"

        elif sistema == "windows":
            subprocess.Popen(f"taskkill /IM {nombre}.exe /F", shell=True)
            return f"Cerrando {nombre.capitalize()}"

        elif sistema == "linux":
            subprocess.Popen(["pkill", nombre])
            return f"Cerrando {nombre.capitalize()}"

        else:
            return f"Sistema operativo no compatible: {sistema}"

    except Exception as e:
        return f"No pude cerrar {nombre}: {str(e)}"

def buscar_archivos(nombre=None, tipo=None, fecha=None, ruta_inicio="~/Documents"):
    ruta_inicio = os.path.expanduser(ruta_inicio)
    resultados = []

    for carpeta_raiz, subcarpetas, archivos in os.walk(ruta_inicio):
        for archivo in archivos:
            ruta_completa = os.path.join(carpeta_raiz, archivo)

            # Filtro por nombre
            if nombre and nombre.lower() not in archivo.lower():
                continue

            # Filtro por tipo
            if tipo and not archivo.lower().endswith(tipo.lower()):
                continue

            # Filtro por fecha de modificación (YYYY-MM-DD)
            if fecha:
                fecha_mod = datetime.datetime.fromtimestamp(os.path.getmtime(ruta_completa)).date()
                try:
                    fecha_obj = datetime.datetime.strptime(fecha, "%Y-%m-%d").date()
                    if fecha_mod != fecha_obj:
                        continue
                except ValueError:
                    continue  # Fecha no válida

            resultados.append(ruta_completa)

    if not resultados:
        return "No se encontraron archivos con los criterios proporcionados."
    
    return "\n".join(resultados[:10])  # Devuelve solo los primeros 10 resultados
