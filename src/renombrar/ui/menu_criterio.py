"""
Módulo de interfaz de usuario para selección del criterio de renombramiento
y confirmaciones interactivas asociadas a metadatos.
"""

CRITERIO_PATRONES = 1
CRITERIO_METADATOS = 2
CRITERIO_SALIR = 3

def seleccionar_criterio_renombrado():
    """Presenta al usuario las opciones de criterio de renombramiento."""
    print("\n" + "=" * 60)
    print("SELECCION DE CRITERIO DE RENOMBRAMIENTO".center(60))
    print("=" * 60)
    print("Por favor, elija como desea analizar y renombrar los archivos:\n")
    print("  1. Busqueda de patrones en el nombre del archivo")
    print("     (Detecta fechas en nombres como IMG_YYYYMMDD_HHMMSS)")
    print()
    print("  2. Busqueda en metadatos de los archivos (Fotos y Videos)")
    print("     (Lee la fecha/hora de captura incrustada en EXIF / contenedores)")
    print()
    print("  3. Salir del programa")
    print("=" * 60)

    while True:
        opcion = input("\nSeleccione una opcion (1-3): ").strip()
        if opcion == "1":
            return CRITERIO_PATRONES
        if opcion == "2":
            return CRITERIO_METADATOS
        if opcion == "3":
            return CRITERIO_SALIR
        print("Opcion no valida. Por favor, ingrese 1, 2 o 3.")

def confirmar_renombrado_sin_hora(nombre_archivo, nuevo_nombre_propuesto):
    """Notifica que no se encontró la hora en los metadatos y solicita confirmación."""
    print("\n" + "-" * 60)
    print(f"AVISO: No se encontro informacion de hora para: {nombre_archivo}")
    print(f"Propuesta sin hora: {nuevo_nombre_propuesto}")
    print("-" * 60)

    while True:
        respuesta = input("Desea renombrar este archivo solo con la fecha? (s/n): ").lower().strip()
        if respuesta in ("s", "si"):
            return True
        if respuesta in ("n", "no"):
            return False
        print("Por favor, responda con 's' para si o 'n' para no.")

def preguntar_usar_fallback(archivos_sin_metadatos):
    """
    Advierte que se encontraron archivos sin metadatos, los lista agrupados por carpeta,
    y consulta si desea aplicar el mecanismo de fallback (búsqueda de patrones en el nombre).
    """
    if isinstance(archivos_sin_metadatos, dict):
        total = sum(len(lista) for lista in archivos_sin_metadatos.values())
    else:
        total = int(archivos_sin_metadatos)

    print("\n" + "!" * 60)
    print(f"ADVERTENCIA: Se encontraron {total} archivo(s) sin metadatos de fecha.".center(60))
    print("!" * 60)

    if isinstance(archivos_sin_metadatos, dict):
        print("\nListado de archivos sin metadatos de fecha:")
        for dir_rel, lista in archivos_sin_metadatos.items():
            if lista:
                nombre_dir = dir_rel if dir_rel != '.' else 'Directorio actual'
                print(f"\n  Carpeta: [{nombre_dir}] ({len(lista)} archivo(s)):")
                for nombre in lista:
                    print(f"    - {nombre}")

    print("\nPuede intentar renombrarlos usando la busqueda de patrones en sus nombres (fallback).")

    while True:
        respuesta = input("\nDesea aplicar fallback a estos archivos? (s/n): ").lower().strip()
        if respuesta in ("s", "si"):
            return True
        if respuesta in ("n", "no"):
            return False
        print("Por favor, responda con 's' para si o 'n' para no.")
