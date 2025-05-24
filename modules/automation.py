# modules/automation.py
import os
import platform
import subprocess


def handle_automation(command):
    sistema = platform.system()

    if any(word in command for word in ["chrome", "navegador"]):
        return abrir_aplicacion("chrome" if sistema == "Windows" else "google chrome")

    elif any(word in command for word in ["visual studio", "vs code", "code"]):
        return abrir_aplicacion("code")

    elif "calculadora" in command:
        if sistema == "Windows":
            return abrir_aplicacion("calc")
        elif sistema == "Darwin":  # macOS
            return abrir_aplicacion("open -a Calculator")

    elif "spotify" in command:
        if sistema == "Windows":
            return abrir_aplicacion("spotify")
        elif sistema == "Darwin":
            return abrir_aplicacion("open -a Spotify")

    else:
        return "No tengo esa aplicación registrada."


def abrir_aplicacion(app):
    try:
        subprocess.Popen(app if isinstance(app, list) else app.split())
        return f"Abriendo {app}..."
    except Exception as e:
        return f"Error al abrir {app}: {str(e)}"
