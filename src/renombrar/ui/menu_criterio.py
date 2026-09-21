"""
Módulo de interfaz de usuario para selección del criterio de renombramiento
y confirmaciones interactivas asociadas a metadatos.
"""

CRITERIO_PATRONES = 1
CRITERIO_METADATOS = 2
CRITERIO_SALIR = 3

def seleccionar_criterio_renombrado():
    """
    Presenta al usuario las opciones de criterio de renombramiento
    antes de comenzar la búsqueda de archivos.
    Retorna CRITERIO_PATRONES, CRITERIO_METADATOS o CRITERIO_SALIR.
    """
    print("\n" + "=" * 60)
    print("SELECCIÓN DE CRITERIO DE RENOMBRAMIENTO".center(60))
    print("=" * 60)
    print("Por favor, elija cómo desea analizar y renombrar los archivos:\n")
    print("  1. Búsqueda de patrones en el nombre del archivo")
    print("     (Detecta fechas en nombres como IMG_YYYYMMDD_HHMMSS)")
    print()
    print("  2. Búsqueda en metadatos de los archivos (Fotos y Videos)")
    print("     (Lee la fecha/hora de captura incrustada en EXIF / contenedores)")
    print()
    print("  3. Salir del programa")
    print("=" * 60)

    while True:
        opcion = input("\nSeleccione una opción (1-3): ").strip()
        if opcion == "1":
            return CRITERIO_PATRONES
        if opcion == "2":
            return CRITERIO_METADATOS
        if opcion == "3":
            return CRITERIO_SALIR
        print("Opción no válida. Por favor, ingrese 1, 2 o 3.")

def confirmar_renombrado_sin_hora(nombre_archivo, nuevo_nombre_propuesto):
    """
    Notifica que no se encontró la hora en los metadatos y solicita confirmación
    mostrando cómo quedará el nombre antes de aplicar el cambio.
    """
    print("\n" + "-" * 60)
    print(f"AVISO: No se encontró información de hora para: {nombre_archivo}")
    print(f"Propuesta sin hora: {nuevo_nombre_propuesto}")
    print("-" * 60)

    while True:
        respuesta = input("¿Desea renombrar este archivo solo con la fecha? (s/n): ").lower().strip()
        if respuesta in ("s", "si", "sí"):
            return True
        if respuesta in ("n", "no"):
            return False
        print("Por favor, responda con 's' para sí o 'n' para no.")

def preguntar_usar_fallback(cantidad_sin_metadatos):
    """
    Advierte que se encontraron archivos sin metadatos y consulta si desea
    aplicar el mecanismo de fallback (búsqueda de patrones en el nombre).
    """
    print("\n" + "!" * 60)
    print(f"ADVERTENCIA: Se encontraron {cantidad_sin_metadatos} archivo(s) sin metadatos de fecha.")
    print("!" * 60)
    print("Puede intentar renombrarlos usando la búsqueda de patrones en sus nombres (fallback).")

    while True:
        respuesta = input("¿Desea aplicar fallback a estos archivos? (s/n): ").lower().strip()
        if respuesta in ("s", "si", "sí"):
            return True
        if respuesta in ("n", "no"):
            return False
        print("Por favor, responda con 's' para sí o 'n' para no.")
