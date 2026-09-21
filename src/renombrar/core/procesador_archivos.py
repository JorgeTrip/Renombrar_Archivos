"""
Módulo procesador y clasificador de archivos para renombrado por lotes.
Separa la lógica de orquestación de la interfaz de usuario.
"""

import os
from .file_utils import (
    obtener_nombre_destino,
    formatear_nombre_destino,
    renombrar_archivo
)
from .date_utils import tiene_formato_telefono

def clasificar_archivos_por_patron(archivos_por_dir, dirs_seleccionados, exts_permitidas):
    """Clasifica los archivos detectados por patrones de nombre."""
    clasificados = {
        'archivos_img': [], 'archivos_vid': [], 'otros_archivos': [],
        'archivos_telefono': [], 'archivos_sugeridos': []
    }
    secuencia = 0
    for dir_rel in dirs_seleccionados:
        for nombre in archivos_por_dir.get(dir_rel, []):
            nuevo = obtener_nombre_destino(nombre, secuencia)
            if nombre == nuevo:
                continue
            secuencia += 1
            info = (dir_rel, nombre, nuevo)
            nombre_upper = nombre.upper()
            if not nombre.lower().endswith(exts_permitidas):
                clasificados['archivos_sugeridos'].append(info)
            elif tiene_formato_telefono(nombre):
                clasificados['archivos_telefono'].append(info)
            elif nombre_upper.startswith("IMG"):
                clasificados['archivos_img'].append(info)
            elif nombre_upper.startswith("VID"):
                clasificados['archivos_vid'].append(info)
            else:
                clasificados['otros_archivos'].append(info)
    return clasificados

def clasificar_archivos_por_metadatos(archivos_por_dir, dirs_seleccionados, exts_permitidas, callback_sin_hora=None):
    """
    Clasifica los archivos detectados por metadatos.
    Cada elemento en archivos_por_dir[dir_rel] es (nombre, fecha, hora).
    """
    clasificados = {
        'archivos_img': [], 'archivos_vid': [], 'otros_archivos': [],
        'archivos_telefono': [], 'archivos_sugeridos': []
    }
    exts_video = (".mp4", ".mkv", ".mov", ".avi", ".wmv", ".flv", ".webm", ".m4v", ".3gp")
    for dir_rel in dirs_seleccionados:
        for item in archivos_por_dir.get(dir_rel, []):
            nombre, fecha, hora = item
            nuevo = formatear_nombre_destino(nombre, fecha, hora)
            if nombre == nuevo:
                continue

            # Si no tiene hora, solicitar confirmación interactiva si existe callback
            if hora is None and callback_sin_hora:
                aceptar = callback_sin_hora(nombre, nuevo)
                if not aceptar:
                    continue

            info = (dir_rel, nombre, nuevo)
            nombre_lower = nombre.lower()
            nombre_upper = nombre.upper()

            if not nombre_lower.endswith(exts_permitidas):
                clasificados['archivos_sugeridos'].append(info)
            elif tiene_formato_telefono(nombre):
                clasificados['archivos_telefono'].append(info)
            elif nombre_lower.endswith(exts_video) or nombre_upper.startswith("VID"):
                clasificados['archivos_vid'].append(info)
            elif nombre_upper.startswith("IMG") or not nombre_lower.endswith(exts_video):
                clasificados['archivos_img'].append(info)
            else:
                clasificados['otros_archivos'].append(info)
    return clasificados

def _generar_nombre_con_sufijo(nuevo_nombre, letra):
    """Inserta una letra sufijo antes de la extensión del archivo."""
    base, ext = os.path.splitext(nuevo_nombre)
    return f"{base}{letra}{ext}"

def ejecutar_renombrado_lote(archivos_a_procesar, dir_base, callback_duplicado):
    """
    Ejecuta el renombrado sobre la lista de archivos seleccionados.
    Gestiona colisiones de nombres mediante letras secuenciales o salto.
    """
    renombrados = 0
    cambios = []

    for dir_rel, original, nuevo_propuesto in archivos_a_procesar:
        dir_abs = os.path.abspath(os.path.join(dir_base, dir_rel))
        ruta_orig = os.path.join(dir_abs, original)
        ruta_dest = os.path.join(dir_abs, nuevo_propuesto)
        nuevo_final = nuevo_propuesto

        if os.path.exists(ruta_dest) and ruta_orig != ruta_dest:
            opcion = callback_duplicado(original, nuevo_propuesto)
            if opcion == 'a':
                letra_codigo = ord('a')
                while os.path.exists(ruta_dest):
                    nuevo_final = _generar_nombre_con_sufijo(nuevo_propuesto, chr(letra_codigo))
                    ruta_dest = os.path.join(dir_abs, nuevo_final)
                    letra_codigo += 1
                if renombrar_archivo(ruta_orig, ruta_dest):
                    renombrados += 1
                    cambios.append((original, nuevo_final))
            # Si es opción 'b' o saltar, se omite
        else:
            if renombrar_archivo(ruta_orig, ruta_dest):
                renombrados += 1
                cambios.append((original, nuevo_final))

    return renombrados, cambios
