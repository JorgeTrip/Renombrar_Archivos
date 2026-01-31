import os
from collections import defaultdict
from .date_utils import obtener_fecha_hora, tiene_formato_telefono

def obtener_nombre_destino(nombre_archivo, secuencia):
    """Genera el nuevo nombre para el archivo basado en su fecha y hora."""
    fecha, hora = obtener_fecha_hora(nombre_archivo)

    if fecha:
        nombre_base, extension = os.path.splitext(nombre_archivo)
        if hora:
            return f"{fecha} {hora} - {nombre_base}{extension}"
        else:
            secuencia = secuencia + 1
            return f"{fecha} - {nombre_base}{extension}"
    return nombre_archivo

def obtener_nombre_destino_letra(nombre_archivo, letra):
    """Genera un nuevo nombre para el archivo agregando una letra al final."""
    fecha, hora = obtener_fecha_hora(nombre_archivo)
    
    if fecha and hora:
        nombre_base, extension = os.path.splitext(nombre_archivo)
        return f"{fecha} {hora} - {nombre_base}{letra}{extension}"
    return None

def renombrar_archivo(ruta_original, ruta_destino):
    """Renombra un archivo de ruta_original a ruta_destino."""
    try:
        os.rename(ruta_original, ruta_destino)
        return True
    except Exception as e:
        print(f"Error al renombrar archivo: {e}")
        return False

def encontrar_archivos_por_directorio(directorio_base):
    """
    Busca todos los archivos con patrones de fecha reconocibles en el directorio base y subdirectorios,
    y los agrupa por su directorio relativo.
    Solo retorna archivos que pueden ser renombrados (tienen fecha extraíble).
    """
    archivos_encontrados = defaultdict(list)
    for directorio_actual, _, archivos in os.walk(directorio_base):
        for nombre_archivo in archivos:
            # Solo agregar el archivo si tiene un patrón de fecha reconocible
            fecha, _ = obtener_fecha_hora(nombre_archivo)
            if fecha:  # Solo incluir archivos con fecha extraíble
                dir_relativo = os.path.relpath(directorio_actual, directorio_base)
                archivos_encontrados[dir_relativo].append(nombre_archivo)
                
    return dict(archivos_encontrados)