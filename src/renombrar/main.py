"""
Módulo principal y orquestador CLI de la aplicación de renombrado de fotos y videos.
Cumple con la Regla de Hierro (menos de 200 líneas de código).
"""

import os

from renombrar.core.file_utils import (
    encontrar_archivos_por_directorio,
    encontrar_archivos_por_metadatos
)
from renombrar.core.date_utils import obtener_fecha_hora
from renombrar.core.procesador_archivos import (
    clasificar_archivos_por_patron,
    clasificar_archivos_por_metadatos,
    ejecutar_renombrado_lote
)
from renombrar.ui.menu import (
    seleccionar_directorios,
    mostrar_resumen_archivos,
    mostrar_menu,
    mostrar_opciones_duplicado,
    preguntar_continuar,
    mostrar_titulo,
    mostrar_bienvenida,
    mostrar_copyright_salida,
    mostrar_aviso_ya_formateados,
    mostrar_previsualizacion_y_confirmar
)
from renombrar.ui.menu_criterio import (
    seleccionar_criterio_renombrado,
    confirmar_renombrado_sin_hora,
    preguntar_opcion_sin_metadatos,
    OPCION_SIN_META_FALLBACK,
    CRITERIO_PATRONES,
    CRITERIO_METADATOS,
    CRITERIO_SALIR
)

EXTENSIONES_PERMITIDAS = (
    ".jpg", ".jpeg", ".png", ".heic", ".heif", ".webp", ".tiff", ".tif",
    ".mp4", ".mkv", ".mov", ".avi", ".wmv", ".flv", ".webm", ".m4v", ".3gp"
)

def _resolver_escaneo(criterio, dir_base):
    """Ejecuta el escaneo y retorna (archivos, criterio, omitidos, fallback_por_dir)."""
    if criterio == CRITERIO_PATRONES:
        archivos, omitidos = encontrar_archivos_por_directorio(dir_base)
        return archivos, criterio, omitidos, None

    con_meta, sin_meta, omitidos = encontrar_archivos_por_metadatos(dir_base, EXTENSIONES_PERMITIDAS)
    total_sin_meta = sum(len(archivos) for archivos in sin_meta.values())
    fallback_por_dir = None

    if total_sin_meta > 0:
        decision = preguntar_opcion_sin_metadatos(sin_meta)
        if decision == OPCION_SIN_META_FALLBACK:
            fallback_por_dir = {}
            for dir_rel, nombres in sin_meta.items():
                for nombre in nombres:
                    fecha, hora = obtener_fecha_hora(nombre)
                    if fecha:
                        fallback_por_dir.setdefault(dir_rel, []).append((nombre, fecha, hora))

    return con_meta, criterio, omitidos, fallback_por_dir

def _mostrar_pantalla_sin_archivos(dir_base):
    """Muestra aviso si no se encontraron archivos candidatos."""
    print("=" * 70)
    print("NO SE ENCONTRARON ARCHIVOS NUEVOS PARA RENOMBRAR".center(70))
    print("=" * 70)
    print(f"\nNo se encontraron archivos procesables en: {dir_base}\n")

def _procesar_ciclo(dir_base):
    """Ejecuta un ciclo completo de escaneo, previsualización y renombrado."""
    criterio = seleccionar_criterio_renombrado()
    if criterio == CRITERIO_SALIR:
        return False

    print(f"\nBuscando archivos en '{dir_base}' y subdirectorios...\n")
    archivos_por_dir, criterio_activo, omitidos, fallback_por_dir = _resolver_escaneo(criterio, dir_base)

    mostrar_aviso_ya_formateados(omitidos)

    todos_dirs = dict(archivos_por_dir)
    if fallback_por_dir:
        for d, l in fallback_por_dir.items():
            todos_dirs.setdefault(d, []).extend(l)

    if not todos_dirs:
        _mostrar_pantalla_sin_archivos(dir_base)
        return preguntar_continuar()

    directorios_sel = seleccionar_directorios(todos_dirs)
    if not directorios_sel:
        print("\nNo se seleccionaron directorios.")
        return False

    if criterio_activo == CRITERIO_METADATOS:
        clasificados = clasificar_archivos_por_metadatos(
            archivos_por_dir, directorios_sel, EXTENSIONES_PERMITIDAS,
            callback_sin_hora=confirmar_renombrado_sin_hora,
            archivos_fallback_por_dir=fallback_por_dir
        )
    else:
        clasificados = clasificar_archivos_por_patron(
            archivos_por_dir, directorios_sel, EXTENSIONES_PERMITIDAS
        )

    if not mostrar_resumen_archivos(clasificados):
        return preguntar_continuar()

    categorias_sel = mostrar_menu(clasificados)
    if not categorias_sel:
        print("\nOperación cancelada.")
        return False

    archivos_a_procesar = []
    vistos = set()
    for cat in categorias_sel:
        for item in clasificados.get(cat, []):
            if item not in vistos:
                vistos.add(item)
                archivos_a_procesar.append(item)

    if not archivos_a_procesar:
        print("\nNo hay archivos en las categorías seleccionadas.")
        return preguntar_continuar()

    if not mostrar_previsualizacion_y_confirmar(archivos_a_procesar):
        print("\nOperación cancelada por el usuario. No se modificó ningún archivo.")
        return preguntar_continuar()

    print(f"\nProcediendo con el renombrado de {len(archivos_a_procesar)} archivos...")
    renombrados, cambios = ejecutar_renombrado_lote(
        archivos_a_procesar, dir_base, callback_duplicado=mostrar_opciones_duplicado
    )

    print("\nProceso de cambio de nombre finalizado.")
    print(f"\nSe realizaron {renombrados} cambios:")
    for cambio in cambios:
        print(f"  {cambio[0]} --> {cambio[1]}")
    print("=" * 60)

    return preguntar_continuar()

def main():
    """Punto de entrada principal de la aplicación."""
    dir_base = os.getcwd()

    if not mostrar_bienvenida():
        print("\nPrograma cancelado por el usuario.")
        mostrar_copyright_salida()
        input("\nPresione cualquier tecla para salir...")
        return

    while True:
        mostrar_titulo()
        continuar = _procesar_ciclo(dir_base)
        if not continuar:
            mostrar_copyright_salida()
            input("\nPresione cualquier tecla para salir...")
            break
        print("\n" + "=" * 50 + "\n")