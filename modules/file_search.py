import os
import fnmatch
from datetime import datetime

def buscar_archivos(directorio, nombre=None, extension=None, fecha_modificada=None):
    """
    Busca archivos en un directorio utilizando filtros por voz.
    Procesa comandos de voz para buscar por nombre, extensión y fecha de modificación.

    Args:
        directorio (str): Ruta base donde buscar.
        nombre (str, optional): Nombre o parte del nombre del archivo pronunciado.
        extension (str, optional): Extensión del archivo pronunciada (ej: 'pdf', 'txt').
        fecha_modificada (str, optional): Fecha pronunciada, convertida a formato 'YYYY-MM-DD'.

    Returns:
        list: Lista de archivos que coinciden con los criterios de búsqueda por voz.
              Retorna mensaje de error si no se encuentran coincidencias.
    """
    resultados = []

    if fecha_modificada:
        try:
            fecha_obj = datetime.strptime(fecha_modificada, "%Y-%m-%d").date()
        except ValueError:
            return ["Fecha inválida. Usa el formato YYYY-MM-DD."]

    for root, dirs, files in os.walk(directorio):
        for archivo in files:
            ruta_completa = os.path.join(root, archivo)

            if nombre and nombre.lower() not in archivo.lower():
                continue

            if extension and not archivo.lower().endswith(extension.lower()):
                continue

            if fecha_modificada:
                timestamp_mod = os.path.getmtime(ruta_completa)
                fecha_archivo = datetime.fromtimestamp(timestamp_mod).date()
                if fecha_archivo != fecha_obj:
                    continue

            resultados.append(ruta_completa)

    return resultados if resultados else ["No se encontraron archivos con esos criterios."]
def abrir_archivo(ruta_archivo):
    """
    Abre un archivo con la aplicación predeterminada del sistema.
    Args:
        ruta_archivo (str): Ruta del archivo a abrir.
    """
    if os.path.exists(ruta_archivo):
        os.startfile(ruta_archivo)
    else:
        print(f"El archivo {ruta_archivo} no existe.")
