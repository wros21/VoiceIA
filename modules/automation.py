# modules/automation.py
import os
import platform
import subprocess


def handle_automation(command):
    sistema = platform.system()

    if "navegador" in command:
        return abrir_aplicacion("chrome" if sistema == "Windows" else "google-chrome")
    elif "visual studio" in command or "vs code" in command:
        return abrir_aplicacion("code")
    elif "calculadora" in command:
        if sistema == "Windows":
            return abrir_aplicacion("calc")
        elif sistema == "Darwin":  # macOS
            return abrir_aplicacion("open -a Calculator")
    else:
        return "No tengo esa aplicación registrada."


def abrir_aplicacion(app):
    try:
        subprocess.Popen(app if isinstance(app, list) else app.split())
        return f"Abriendo {app}..."
    except Exception as e:
        return f"Error al abrir {app}: {str(e)}"
