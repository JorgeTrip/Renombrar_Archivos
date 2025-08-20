import os

def seleccionar_directorios(archivos_por_directorio):
    """Muestra los directorios encontrados y permite al usuario seleccionar cuáles procesar."""
    directorios = list(archivos_por_directorio.keys())
    if not directorios:
        print("No se encontraron directorios con archivos que coincidan con los patrones.")
        return []

    print("Se encontraron archivos en los siguientes directorios:")
    for i, ruta in enumerate(directorios):
        nombre_dir = ruta if ruta != '.' else 'Directorio actual'
        print(f"  {i + 1}. {nombre_dir} ({len(archivos_por_directorio[ruta])} archivos)")

    print("\nSeleccione los directorios a procesar:")
    print("  - Para seleccionar varios, sepárelos por comas (ej: 1,3).")
    print("  - Para seleccionar todos, escriba 'todos'.")

    while True:
        seleccion = input("\nOpción: ").lower().strip()
        if seleccion == 'todos':
            return directorios
        
        try:
            indices = [int(i.strip()) - 1 for i in seleccion.split(',')]
            if all(0 <= i < len(directorios) for i in indices):
                return [directorios[i] for i in indices]
            else:
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
                    # Para archivos sugeridos que no se renombran pero coinciden con el patrón
                    print(f"  {ruta_mostrada}")
    
    return True

def mostrar_menu(archivos_clasificados):
    """Muestra el menú principal y obtiene la opción seleccionada."""
    print("\nOpciones de renombrado:")
    opciones = {}
    idx = 1

    # Opción para todos los archivos
    opciones[idx] = ("Todos los archivos", list(archivos_clasificados.keys()))
    print(f"{idx}. Todos los archivos")
    idx += 1

    # Opciones por categoría
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

    # Opción para IMG y VID juntos
    if archivos_clasificados.get('archivos_img') and archivos_clasificados.get('archivos_vid'):
        opciones[idx] = ("Archivos IMG y VID", ['archivos_img', 'archivos_vid'])
        print(f"{idx}. Archivos IMG y VID")
        idx += 1

    # Opción de salida
    opcion_salir = idx
    print(f"{opcion_salir}. Salir sin hacer cambios")

    while True:
        try:
            seleccion = int(input(f"\nSeleccione una opción (1-{opcion_salir}): "))
            if seleccion == opcion_salir:
                return None  # Indicar salida
            if seleccion in opciones:
                return opciones[seleccion][1]  # Devuelve las claves de las categorías a procesar
            print(f"\nPor favor, seleccione una opción válida (1-{opcion_salir})")
        except ValueError:
            print("\nPor favor, ingrese un número válido")

def mostrar_opciones_duplicado(nombre_archivo, nuevo_nombre):
    """Muestra las opciones cuando se encuentra un archivo duplicado."""
    print()
    print(f"Error al intentar renombrar archivo \"{nombre_archivo}\":")
    print(f"El archivo \"{nuevo_nombre}\" ya existe.")
    print()
    print("Opciones:")
    print("a. Renombrar agregando letra al final")
    print("b. No hacer nada (omitir renombrar)")
    
    while True:
        opcion = input("\n¿Qué desea hacer? (a/b): ").lower()
        if opcion in ['a', 'b']:
            return opcion
        print("\nOpción no válida. Por favor, seleccione 'a' o 'b'.")

def preguntar_continuar():
    """Pregunta al usuario si desea continuar renombrando archivos."""
    while True:
        continuar = input("\n¿Desea continuar renombrando archivos? (s/n): ").lower()
        if continuar in ['s', 'n']:
            return continuar == 's'
        print("Por favor, responda con 's' para sí o 'n' para no.") 