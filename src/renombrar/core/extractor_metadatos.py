"""
Módulo para autodetección de formatos y extracción de metadatos de fotos y videos.
Soporta JPEG, PNG, HEIC, TIFF, WebP, MP4, MOV, MKV, AVI y WAV.
"""

import os
from datetime import datetime
from PIL import Image

try:
    import pillow_heif
    pillow_heif.register_heif_opener()
except ImportError:
    pass

try:
    import mutagen
except ImportError:
    mutagen = None

try:
    from hachoir.parser import createParser
    from hachoir.metadata import extractMetadata
except ImportError:
    createParser = None
    extractMetadata = None

# Tipos de formatos detectados
TIPO_IMAGEN_EXIF = "IMAGEN_EXIF"
TIPO_IMAGEN_HEIC = "IMAGEN_HEIC"
TIPO_VIDEO_MUTAGEN = "VIDEO_MUTAGEN"
TIPO_VIDEO_HACHOIR = "VIDEO_HACHOIR"
TIPO_AUDIO_WAV = "AUDIO_WAV"
TIPO_DESCONOCIDO = "DESCONOCIDO"

EXTS_EXIF = {".jpg", ".jpeg", ".png", ".webp", ".tiff", ".tif"}
EXTS_HEIC = {".heic", ".heif"}
EXTS_MUTAGEN = {".mp4", ".mov", ".m4v", ".3gp"}
EXTS_HACHOIR = {".mkv", ".avi", ".wmv", ".flv", ".webm"}

def detectar_tipo_archivo(ruta_archivo):
    """Detecta automáticamente el tipo y librería correspondiente para el archivo."""
    _, ext = os.path.splitext(ruta_archivo.lower())
    if ext in EXTS_EXIF:
        return TIPO_IMAGEN_EXIF
    if ext in EXTS_HEIC:
        return TIPO_IMAGEN_HEIC
    if ext in EXTS_MUTAGEN:
        return TIPO_VIDEO_MUTAGEN
    if ext in EXTS_HACHOIR:
        return TIPO_VIDEO_HACHOIR
    if ext == ".wav":
        return TIPO_AUDIO_WAV
    return TIPO_DESCONOCIDO

def _parsear_cadena_fecha(cadena):
    """Parsea una cadena de fecha/hora en formato (YYYY-MM-DD, HH-MM-SS o None)."""
    if not cadena:
        return None, None
    texto = str(cadena).strip()
    formatos = [
        "%Y:%m:%d %H:%M:%S",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%dT%H:%M:%S",
        "%Y:%m:%d",
        "%Y-%m-%d"
    ]
    for fmt in formatos:
        try:
            dt = datetime.strptime(texto, fmt)
            fecha = dt.strftime("%Y-%m-%d")
            hora = dt.strftime("%H-%M-%S") if ("%H" in fmt) else None
            return fecha, hora
        except ValueError:
            continue
    return None, None

def _extraer_exif_imagen(ruta_archivo):
    """Extrae fecha y hora desde metadatos EXIF con Pillow."""
    try:
        with Image.open(ruta_archivo) as img:
            exif = img.getexif()
            if not exif:
                return None, None
            # Probar DateTimeOriginal (36867), DateTimeDigitized (36868), DateTime (306)
            etiquetas = [36867, 36868, 306]
            # Si tiene ifd Exif (0x8769), consultar allí primero
            try:
                exif_ifd = exif.get_ifd(0x8769)
            except Exception:
                exif_ifd = {}

            for tag in etiquetas:
                valor = exif_ifd.get(tag) or exif.get(tag)
                if valor:
                    fecha, hora = _parsear_cadena_fecha(valor)
                    if fecha:
                        return fecha, hora
    except Exception:
        pass
    return None, None

def _extraer_video_mutagen(ruta_archivo):
    """Extrae metadatos de video mediante mutagen."""
    if not mutagen:
        return None, None
    try:
        medio = mutagen.File(ruta_archivo)
        if medio and medio.tags:
            # MP4 \xa9day tag
            clave_dia = medio.tags.get("\xa9day")
            if clave_dia:
                valor = clave_dia[0] if isinstance(clave_dia, list) else clave_dia
                fecha, hora = _parsear_cadena_fecha(valor)
                if fecha:
                    return fecha, hora
    except Exception:
        pass
    return None, None

def _extraer_video_hachoir(ruta_archivo):
    """Extrae metadatos mediante hachoir como analizador universal."""
    if not createParser or not extractMetadata:
        return None, None
    try:
        parser = createParser(ruta_archivo)
        if not parser:
            return None, None
        with parser:
            metadatos = extractMetadata(parser)
            if metadatos and metadatos.has("creation_date"):
                dt = metadatos.get("creation_date")
                if isinstance(dt, datetime):
                    return dt.strftime("%Y-%m-%d"), dt.strftime("%H-%M-%S")
    except Exception:
        pass
    return None, None

def extraer_metadatos_fecha_hora(ruta_archivo):
    """
    Punto de entrada principal con autodetección de formato y cascada de librerías.
    Retorna tupla (fecha, hora). Si no existe fecha, retorna (None, None).
    """
    if not os.path.exists(ruta_archivo) or not os.path.isfile(ruta_archivo):
        return None, None

    tipo = detectar_tipo_archivo(ruta_archivo)

    if tipo in (TIPO_IMAGEN_EXIF, TIPO_IMAGEN_HEIC):
        return _extraer_exif_imagen(ruta_archivo)

    if tipo == TIPO_VIDEO_MUTAGEN:
        fecha, hora = _extraer_video_mutagen(ruta_archivo)
        if fecha:
            return fecha, hora
        return _extraer_video_hachoir(ruta_archivo)

    if tipo == TIPO_VIDEO_HACHOIR:
        fecha, hora = _extraer_video_hachoir(ruta_archivo)
        if fecha:
            return fecha, hora
        return _extraer_video_mutagen(ruta_archivo)

    return None, None
