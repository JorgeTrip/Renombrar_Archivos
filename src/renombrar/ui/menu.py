"""
Módulo de interfaz de usuario con menús de selección, resumen y salida.
"""

import os
import shutil
import platform

def limpiar_pantalla():
    """Limpia la pantalla de la consola."""
    os.system('cls' if platform.system() == 'Windows' else 'clear')

def mostrar_copyright_salida():
    """Muestra el copyright antes de salir del programa."""
    print("\n" + "=" * 60)
    print("© Jorge Osvaldo Tripodi (JOT) 2025".center(60))
    print("Gracias por usar este programa".center(60))
    print("=" * 60)

def mostrar_titulo():
    """Muestra el título centrado del programa."""
    titulo = "Renombrar archivos de fotos y videos - v1.9"
    subtitulo = "---> by JOT <---"
    copyright_text = "© Jorge Osvaldo Tripodi (JOT) 2025"
    try:
        ancho_terminal = shutil.get_terminal_size().columns
    except Exception:
        ancho_terminal = 80
    separador = "=" * ancho_terminal
    print(separador)
    print(titulo.center(ancho_terminal))
    print(subtitulo.center(ancho_terminal))
    print(copyright_text.center(ancho_terminal))
    print(separador + "\n")

def mostrar_bienvenida():
    """Muestra la pantalla de bienvenida con ejemplos y pide confirmación."""
    mostrar_titulo()
    print("Este programa renombra archivos multimedia agregando fecha y hora al inicio.")
    print("\nCRITERIOS SOPORTADOS:")
    print("  1. Por patrones en el nombre del archivo (IMG_, VID_, formato teléfono)")
    print("  2. Por metadatos incrustados de captura/creación (EXIF / Video)\n")
    print("EJEMPLOS:")
    print("-" * 70)
    print("  • IMG_20230315_143022.jpg   → 2023-03-15 14-30-22 - IMG_20230315_143022.jpg")
    print("  • 20231225_090000.mp4       → 2023-12-25 09-00-00 - 20231225_090000.mp4")
    print("  • VID_20240101_120000.mkv   → 2024-01-01 12-00-00 - VID_20240101_120000.mkv")
    print("-" * 70 + "\n")

    while True:
        respuesta = input("¿Desea continuar con el programa? (s/n): ").lower().strip()
        if respuesta in ['s', 'n']:
            if respuesta == 's':
                limpiar_pantalla()
                return True
            return False
        print("Por favor, responda con 's' para sí o 'n' para no.")

def seleccionar_directorios(archivos_por_directorio):
    """Muestra los directorios encontrados y permite seleccionar cuáles procesar."""
    directorios = list(archivos_por_directorio.keys())
    if not directorios:
        print("No se encontraron directorios con archivos para procesar.")
        return []

    print("Se encontraron archivos en los siguientes directorios:")
    for i, ruta in enumerate(directorios):
        nombre_dir = ruta if ruta != '.' else 'Directorio actual'
        print(f"  {i + 1}. {nombre_dir} ({len(archivos_por_directorio[ruta])} archivos)")

    print("\nSeleccione los directorios a procesar:")
    print("  - Para varios, sepárelos por comas (ej: 1,3). Escriba 'todos' para todos.")

    while True:
        seleccion = input("\nOpción: ").lower().strip()
        if seleccion == 'todos':
            return directorios
        try:
            indices = [int(i.strip()) - 1 for i in seleccion.split(',')]
            if all(0 <= i < len(directorios) for i in indices):
                return [directorios[i] for i in indices]
            print("Error: Uno o más números están fuera de rango.")
        except ValueError:
            print("Error: Entrada no válida. Use números separados por comas o 'todos'.")

def mostrar_resumen_archivos(archivos_clasificados):
    """Muestra un resumen de los archivos encontrados en los directorios seleccionados."""
    total = sum(len(lista) for lista in archivos_clasificados.values())
    if total == 0:
        print("No se encontraron archivos para renombrar en la selección.")
        return False

    print(f"\nSe encontraron {total} archivos en total en los directorios seleccionados:")
    categorias = {
        'archivos_telefono': "[TELÉFONO]",
        'archivos_img': "[IMG]",
        'archivos_vid': "[VID]",
        'otros_archivos': "[OTROS]",
        'archivos_sugeridos': "[SUGERIDOS]"
    }

    for clave, titulo in categorias.items():
        lista_archivos = archivos_clasificados.get(clave, [])
        if lista_archivos:
            print(f"\n{titulo} {len(lista_archivos)} archivos:")
            for dir_rel, original, nuevo in lista_archivos:
                ruta_mostrada = os.path.join(dir_rel, original) if dir_rel != '.' else original
                if original != nuevo:
                    print(f"  {ruta_mostrada} -> {nuevo}")
                else:
                    print(f"  {ruta_mostrada}")
    return True

def mostrar_menu(archivos_clasificados):
    """Muestra el menú principal y obtiene la opción seleccionada."""
    print("\nOpciones de renombrado:")
    opciones = {}
    idx = 1
    opciones[idx] = ("Todos los archivos", list(archivos_clasificados.keys()))
    print(f"{idx}. Todos los archivos")
    idx += 1

    categorias = {
        'archivos_img': "Archivos IMG",
        'archivos_vid': "Archivos VID",
        'archivos_telefono': "Archivos TELEFONO",
        'archivos_sugeridos': "Archivos SUGERIDOS"
    }
    for clave, texto in categorias.items():
        if archivos_clasificados.get(clave):
            opciones[idx] = (texto, [clave])
            print(f"{idx}. {texto}")
            idx += 1

    if archivos_clasificados.get('archivos_img') and archivos_clasificados.get('archivos_vid'):
        opciones[idx] = ("Archivos IMG y VID", ['archivos_img', 'archivos_vid'])
        print(f"{idx}. Archivos IMG y VID")
        idx += 1

    opcion_salir = idx
    print(f"{opcion_salir}. Salir sin hacer cambios")

    while True:
        try:
            seleccion = int(input(f"\nSeleccione una opción (1-{opcion_salir}): "))
            if seleccion == opcion_salir:
                return None
            if seleccion in opciones:
                return opciones[seleccion][1]
            print(f"\nPor favor, seleccione una opción válida (1-{opcion_salir})")
        except ValueError:
            print("\nPor favor, ingrese un número válido")

def mostrar_opciones_duplicado(nombre_archivo, nuevo_nombre):
    """Muestra las opciones cuando se encuentra un archivo duplicado."""
    print(f"\nError al intentar renombrar archivo \"{nombre_archivo}\":")
    print(f"El archivo \"{nuevo_nombre}\" ya existe.")
    print("Opciones:\n  a. Renombrar agregando letra al final\n  b. No hacer nada (omitir)")
    while True:
        opcion = input("\n¿Qué desea hacer? (a/b): ").lower().strip()
        if opcion in ['a', 'b']:
            return opcion
        print("Opción no válida. Por favor, seleccione 'a' o 'b'.")

def preguntar_continuar():
    """Pregunta al usuario si desea continuar renombrando archivos."""
    while True:
        continuar = input("\n¿Desea continuar renombrando archivos? (s/n): ").lower().strip()
        if continuar in ['s', 'n']:
            return continuar == 's'
        print("Por favor, responda con 's' para sí o 'n' para no.")