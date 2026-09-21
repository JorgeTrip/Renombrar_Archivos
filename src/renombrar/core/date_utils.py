"""
Módulo de utilidades para extracción, verificación y limpieza de fechas en nombres de archivos.
"""

import re
import datetime
import wave
import os

PATRON_DESTINO_COMPLETO = re.compile(r'^\d{4}-\d{2}-\d{2}\s\d{2}-\d{2}-\d{2}.*$')
PATRON_DESTINO_SOLO_FECHA = re.compile(r'^\d{4}-\d{2}-\d{2}(?:[\s\-_].*|\..+)?$')

def tiene_formato_destino_completo(nombre_archivo):
    """Verifica si el archivo ya tiene el formato de destino completo (YYYY-MM-DD HH-MM-SS)."""
    return PATRON_DESTINO_COMPLETO.match(nombre_archivo) is not None

def tiene_formato_destino_solo_fecha(nombre_archivo):
    """Verifica si el archivo tiene el formato de destino solo con fecha (YYYY-MM-DD)."""
    if tiene_formato_destino_completo(nombre_archivo):
        return False
    return PATRON_DESTINO_SOLO_FECHA.match(nombre_archivo) is not None

def limpiar_prefijo_fecha_existente(nombre_archivo):
    """Remueve cualquier prefijo de formato destino previo de forma flexible."""
    patron_completo = r'^\d{4}-\d{2}-\d{2}\s\d{2}-\d{2}-\d{2}(?:\s-\s|[\s\-_])?(.*)$'
    match_completo = re.match(patron_completo, nombre_archivo)
    if match_completo and match_completo.group(1):
        return match_completo.group(1).strip()

    patron_solo_fecha = r'^\d{4}-\d{2}-\d{2}(?:\s-\s|[\s\-_])?(.*)$'
    match_fecha = re.match(patron_solo_fecha, nombre_archivo)
    if match_fecha and match_fecha.group(1):
        return match_fecha.group(1).strip()

    return nombre_archivo

def obtener_fecha_hora(nombre_archivo):
    """Obtiene la fecha y hora del archivo basado en su nombre o metadatos."""
    if nombre_archivo.lower().endswith(".wav"):
        return obtener_fecha_hora_wav(nombre_archivo)
    return obtener_fecha_hora_desde_nombre(nombre_archivo)

def obtener_fecha_hora_wav(nombre_archivo):
    """Obtiene la fecha de creación de un archivo WAV."""
    try:
        with wave.open(nombre_archivo, 'rb'):
            timestamp = os.path.getctime(nombre_archivo)
            fecha_creacion = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H-%M-%S')
            return fecha_creacion, None
    except Exception as e:
        print(f"Error al obtener la fecha de creación para {nombre_archivo}: {e}")
        return None, None

def obtener_fecha_hora_desde_nombre(nombre_archivo):
    """Extrae la fecha y hora del nombre del archivo usando expresiones regulares."""
    patron = r'(\d{4})[-_.\s]?(\d{2})[-_.\s]?(\d{2})(?:.*?(\d{2})[-_.\s]?(\d{2})[-_.\s]?(\d{2}))?'
    coincidencia = re.search(patron, nombre_archivo)
    if coincidencia:
        fecha = f"{coincidencia.group(1)}-{coincidencia.group(2)}-{coincidencia.group(3)}"
        if coincidencia.group(4) and coincidencia.group(5) and coincidencia.group(6):
            hora = f"{coincidencia.group(4)}-{coincidencia.group(5)}-{coincidencia.group(6)}"
        else:
            hora = None
        return fecha, hora
    return None, None

def archivo_tiene_formato_destino(nombre_archivo):
    """Verifica si el archivo ya tiene el formato de nombre de destino."""
    return tiene_formato_destino_completo(nombre_archivo)

def tiene_formato_telefono(nombre_archivo):
    """Verifica si el archivo tiene el formato de nombre de teléfono."""
    patron_telefono = r'^\d{8}_\d{6}\.'
    return re.match(patron_telefono, nombre_archivo) is not None