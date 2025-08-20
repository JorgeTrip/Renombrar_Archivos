"""
Módulo core que contiene la lógica principal del programa.
"""

from .date_utils import (
    obtener_fecha_hora,
    obtener_fecha_hora_wav,
    obtener_fecha_hora_desde_nombre,
    archivo_tiene_formato_destino,
    tiene_formato_telefono
)
from .file_utils import (
    obtener_nombre_destino,
    obtener_nombre_destino_letra,
    renombrar_archivo,
    encontrar_archivos_por_directorio
)

__all__ = [
    "obtener_fecha_hora",
    "obtener_fecha_hora_wav",
    "obtener_fecha_hora_desde_nombre",
    "archivo_tiene_formato_destino",
    "tiene_formato_telefono",
    "obtener_nombre_destino",
    "obtener_nombre_destino_letra",
    "renombrar_archivo",
    "encontrar_archivos_por_directorio"
] 