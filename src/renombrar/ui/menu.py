"""
Módulo de interfaz de usuario con menús de selección, resumen, previsualización y salida.
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
    print("Jorge Osvaldo Tripodi (JOT) 2025".center(60))
    print("Gracias por usar este programa".center(60))
    print("=" * 60)

def mostrar_titulo():
    """Muestra el título centrado del programa."""
    titulo = "Renombrar archivos de fotos y videos - v1.9"
    subtitulo = "---> by JOT <---"
    copyright_text = "(C) Jorge Osvaldo Tripodi (JOT) 2025"
    try:
        ancho = shutil.get_terminal_size().columns
    except Exception:
        ancho = 80
    sep = "=" * ancho
    print(f"{sep}\n{titulo.center(ancho)}\n{subtitulo.center(ancho)}\n{copyright_text.center(ancho)}\n{sep}\n")

def mostrar_bienvenida():
    """Muestra la pantalla de bienvenida con ejemplos y pide confirmación."""
    mostrar_titulo()
    print("Este programa renombra archivos multimedia agregando fecha y hora al inicio.")
    print("\nCRITERIOS SOPORTADOS:")
    print("  1. Por patrones en el nombre del archivo (IMG_, VID_, formato telefono)")
    print("  2. Por metadatos incrustados de captura/creacion (EXIF / Video)\n")
    print("EJEMPLOS:")
    print("-" * 70)
    print("  * IMG_20230315_143022.jpg   -> 2023-03-15 14-30-22 - IMG_20230315_143022.jpg")
    print("  * 20231225_090000.mp4       -> 2023-12-25 09-00-00 - 20231225_090000.mp4")
    print("-" * 70 + "\n")

    while True:
        resp = input("Desea continuar con el programa? (s/n): ").lower().strip()
        if resp in ['s', 'n']:
            if resp == 's':
                limpiar_pantalla()
                return True
            return False
        print("Por favor, responda con 's' para si o 'n' para no.")

def seleccionar_directorios(archivos_por_directorio):
    """Muestra los directorios encontrados y permite seleccionar cuáles procesar."""
    dirs = list(archivos_por_directorio.keys())
    if not dirs:
        print("No se encontraron directorios con archivos para procesar.")
        return []

    print("Se encontraron archivos en los siguientes directorios:")
    for i, ruta in enumerate(dirs):
        nombre = ruta if ruta != '.' else 'Directorio actual'
        print(f"  {i + 1}. {nombre} ({len(archivos_por_directorio[ruta])} archivos)")

    print("\nSeleccione los directorios a procesar (ej: 1,3 o 'todos'):")
    while True:
        sel = input("\nOpcion: ").lower().strip()
        if sel == 'todos':
            return dirs
        try:
            indices = [int(i.strip()) - 1 for i in sel.split(',')]
            if all(0 <= i < len(dirs) for i in indices):
                return [dirs[i] for i in indices]
            print("Error: Uno o mas numeros estan fuera de rango.")
        except ValueError:
            print("Error: Entrada no valida. Use numeros separados por comas o 'todos'.")

def mostrar_aviso_ya_formateados(cantidad):
    """Muestra un mensaje informativo si se omitieron archivos ya formateados."""
    if cantidad > 0:
        print(f"\n[INFO] Se encontraron {cantidad} archivo(s) que ya tienen el formato destino (YYYY-MM-DD HH-MM-SS) y fueron omitidos.")

def mostrar_resumen_archivos(archivos_clasificados):
    """Muestra un resumen de los archivos encontrados en los directorios seleccionados."""
    total = sum(len(l) for k, l in archivos_clasificados.items() if k not in ('archivos_con_metadatos', 'archivos_fallback'))
    if total == 0:
        total = sum(len(l) for l in archivos_clasificados.values())
    if total == 0:
        print("No se encontraron archivos para renombrar en la seleccion.")
        return False

    print(f"\nSe encontraron {total} archivos en total para procesar en los directorios seleccionados:")
    titulos = {
        'archivos_telefono': "[TELEFONO]", 'archivos_img': "[IMG]",
        'archivos_vid': "[VID]", 'otros_archivos': "[OTROS]", 'archivos_sugeridos': "[SUGERIDOS]"
    }
    for clave, tit in titulos.items():
        lista = archivos_clasificados.get(clave, [])
        if lista:
            print(f"\n{tit} {len(lista)} archivos:")
            for dir_rel, orig, nuevo in lista:
                ruta = os.path.join(dir_rel, orig) if dir_rel != '.' else orig
                print(f"  {ruta} -> {nuevo}" if orig != nuevo else f"  {ruta}")
    return True

def mostrar_menu(archivos_clasificados):
    """Muestra el menú principal y obtiene la opción seleccionada."""
    print("\nOpciones de renombrado:")
    cats_formato = [k for k in ['archivos_img', 'archivos_vid', 'archivos_telefono', 'otros_archivos', 'archivos_sugeridos'] if archivos_clasificados.get(k)]
    todas = cats_formato if cats_formato else list(archivos_clasificados.keys())
    opciones = {1: ("Todos los archivos", todas)}
    print("1. Todos los archivos")
    idx = 2

    # Segmentación opcional entre metadatos y fallback
    if archivos_clasificados.get('archivos_con_metadatos') and archivos_clasificados.get('archivos_fallback'):
        cant_meta = len(archivos_clasificados['archivos_con_metadatos'])
        cant_fall = len(archivos_clasificados['archivos_fallback'])
        opciones[idx] = (f"Solo archivos con metadatos ({cant_meta})", ['archivos_con_metadatos'])
        print(f"{idx}. Solo archivos con metadatos ({cant_meta})")
        idx += 1
        opciones[idx] = (f"Solo archivos por fallback ({cant_fall})", ['archivos_fallback'])
        print(f"{idx}. Solo archivos por fallback ({cant_fall})")
        idx += 1

    for clave, txt in [('archivos_img', "Archivos IMG"), ('archivos_vid', "Archivos VID"),
                       ('archivos_telefono', "Archivos TELEFONO"), ('archivos_sugeridos', "Archivos SUGERIDOS")]:
        if archivos_clasificados.get(clave):
            opciones[idx] = (txt, [clave])
            print(f"{idx}. {txt}")
            idx += 1

    if archivos_clasificados.get('archivos_img') and archivos_clasificados.get('archivos_vid'):
        opciones[idx] = ("Archivos IMG y VID", ['archivos_img', 'archivos_vid'])
        print(f"{idx}. Archivos IMG y VID")
        idx += 1

    opc_salir = idx
    print(f"{opc_salir}. Salir sin hacer cambios")
    while True:
        try:
            sel = int(input(f"\nSeleccione una opcion (1-{opc_salir}): "))
            if sel == opc_salir:
                return None
            if sel in opciones:
                return opciones[sel][1]
            print(f"Opcion invalida (1-{opc_salir})")
        except ValueError:
            print("Ingrese un numero valido")

def mostrar_previsualizacion_y_confirmar(archivos_a_procesar):
    """Muestra previsualización exacta de los archivos a modificar y pide confirmación."""
    total = len(archivos_a_procesar)
    print("\n" + "=" * 70)
    print(f"PREVISUALIZACION DE CAMBIOS ({total} archivos a renombrar)".center(70))
    print("=" * 70)
    for dir_rel, orig, nuevo in archivos_a_procesar:
        ruta = os.path.join(dir_rel, orig) if dir_rel != '.' else orig
        print(f"  {ruta}  ->  {nuevo}")
    print("=" * 70)

    while True:
        resp = input(f"\nDesea proceder a renombrar estos {total} archivos? (s/n): ").lower().strip()
        if resp in ('s', 'si'):
            return True
        if resp in ('n', 'no'):
            return False
        print("Por favor, responda con 's' para si o 'n' para no.")

def mostrar_opciones_duplicado(nombre, nuevo):
    """Muestra las opciones cuando se encuentra un archivo duplicado."""
    print(f"\nError: \"{nuevo}\" ya existe para \"{nombre}\".\nOpciones:\n  a. Sufijo alfabetico\n  b. Omitir")
    while True:
        opc = input("Opcion (a/b): ").lower().strip()
        if opc in ['a', 'b']:
            return opc

def preguntar_continuar():
    """Pregunta al usuario si desea continuar en el programa."""
    while True:
        resp = input("\nDesea continuar renombrando archivos? (s/n): ").lower().strip()
        if resp in ['s', 'n']:
            return resp == 's'