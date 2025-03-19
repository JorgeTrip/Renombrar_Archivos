import os
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

def buscar_archivos(directorio, extensiones_permitidas):
    """Busca archivos en el directorio y sus subdirectorios."""
    archivos_img = []
    archivos_vid = []
    otros_archivos = []
    archivos_telefono = []
    
    for directorio_raiz, _, archivos in os.walk(directorio):
        for nombre_archivo in archivos:
            if nombre_archivo.lower().endswith(extensiones_permitidas):
                archivo_info = (directorio_raiz, nombre_archivo)
                nombre_upper = nombre_archivo.upper()
                
                if tiene_formato_telefono(nombre_archivo):
                    archivos_telefono.append(archivo_info)
                elif nombre_upper.startswith("IMG"):
                    archivos_img.append(archivo_info)
                elif nombre_upper.startswith("VID"):
                    archivos_vid.append(archivo_info)
                else:
                    otros_archivos.append(archivo_info)
    
    return archivos_img, archivos_vid, otros_archivos, archivos_telefono 