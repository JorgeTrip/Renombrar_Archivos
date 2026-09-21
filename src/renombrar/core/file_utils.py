"""
Módulo de utilidades de archivos para búsqueda, generación de nombres y renombrado.
Soporta tanto el criterio por patrones en el nombre como por metadatos multimedia.
"""

import os
from collections import defaultdict
from .date_utils import (
    obtener_fecha_hora,
    tiene_formato_destino_completo,
    tiene_formato_destino_solo_fecha,
    limpiar_prefijo_fecha_existente
)
from .extractor_metadatos import extraer_metadatos_fecha_hora

def formatear_nombre_destino(nombre_archivo, fecha, hora):
    """Genera el nuevo nombre a partir de una fecha y hora explícitas, limpiando prefijos previos."""
    if not fecha:
        return nombre_archivo
    nombre_limpio = limpiar_prefijo_fecha_existente(nombre_archivo)
    nombre_base, extension = os.path.splitext(nombre_limpio)
    if hora:
        return f"{fecha} {hora} - {nombre_base}{extension}"
    return f"{fecha} - {nombre_base}{extension}"

def formatear_nombre_destino_letra(nombre_archivo, fecha, hora, letra):
    """Genera un nuevo nombre agregando un sufijo de letra para evitar colisiones."""
    if not fecha:
        return None
    nombre_limpio = limpiar_prefijo_fecha_existente(nombre_archivo)
    nombre_base, extension = os.path.splitext(nombre_limpio)
    if hora:
        return f"{fecha} {hora} - {nombre_base}{letra}{extension}"
    return f"{fecha} - {nombre_base}{letra}{extension}"

def obtener_nombre_destino(nombre_archivo, secuencia=0):
    """Genera el nuevo nombre para el archivo basado en su fecha y hora extraída del nombre."""
    fecha, hora = obtener_fecha_hora(nombre_archivo)
    return formatear_nombre_destino(nombre_archivo, fecha, hora)

def obtener_nombre_destino_letra(nombre_archivo, letra):
    """Genera un nuevo nombre para el archivo agregando una letra al final."""
    fecha, hora = obtener_fecha_hora(nombre_archivo)
    return formatear_nombre_destino_letra(nombre_archivo, fecha, hora, letra)

def renombrar_archivo(ruta_original, ruta_destino):
    """Renombra un archivo de ruta_original a ruta_destino de forma segura."""
    try:
        os.rename(ruta_original, ruta_destino)
        return True
    except Exception as e:
        print(f"Error al renombrar archivo: {e}")
        return False

def encontrar_archivos_por_directorio(directorio_base):
    """
    Busca archivos con patrones reconocibles omitiendo los que ya tienen formato destino.
    Retorna: (dict con archivos candidatos por dir_rel, total_omitidos_ya_formateados)
    """
    archivos_encontrados = defaultdict(list)
    omitidos = 0
    for directorio_actual, _, archivos in os.walk(directorio_base):
        dir_relativo = os.path.relpath(directorio_actual, directorio_base)
        for nombre_archivo in archivos:
            if tiene_formato_destino_completo(nombre_archivo) or tiene_formato_destino_solo_fecha(nombre_archivo):
                omitidos += 1
                continue
            fecha, _ = obtener_fecha_hora(nombre_archivo)
            if fecha:
                archivos_encontrados[dir_relativo].append(nombre_archivo)
                
    return dict(archivos_encontrados), omitidos

def encontrar_archivos_por_metadatos(directorio_base, extensiones_permitidas):
    """
    Busca archivos con metadatos de fecha omitiendo los ya formateados por completo,
    pero permitiendo enriquecer con hora los que sólo tienen fecha.
    Retorna: (archivos_con_metadatos, archivos_sin_metadatos, total_omitidos_ya_formateados)
    """
    archivos_con_metadatos = defaultdict(list)
    archivos_sin_metadatos = defaultdict(list)
    omitidos = 0

    for directorio_actual, _, archivos in os.walk(directorio_base):
        dir_relativo = os.path.relpath(directorio_actual, directorio_base)
        for nombre_archivo in archivos:
            if not nombre_archivo.lower().endswith(extensiones_permitidas):
                continue
            if tiene_formato_destino_completo(nombre_archivo):
                omitidos += 1
                continue

            ruta_completa = os.path.join(directorio_actual, nombre_archivo)
            fecha, hora = extraer_metadatos_fecha_hora(ruta_completa)

            # Si ya tiene solo fecha, verificar si tiene hora para agregar
            if tiene_formato_destino_solo_fecha(nombre_archivo):
                if hora:
                    archivos_con_metadatos[dir_relativo].append((nombre_archivo, fecha or "", hora))
                else:
                    omitidos += 1
                continue

            if fecha:
                archivos_con_metadatos[dir_relativo].append((nombre_archivo, fecha, hora))
            else:
                archivos_sin_metadatos[dir_relativo].append(nombre_archivo)

    return dict(archivos_con_metadatos), dict(archivos_sin_metadatos), omitidos