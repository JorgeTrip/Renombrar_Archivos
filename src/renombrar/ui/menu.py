def mostrar_resumen_archivos(archivos_telefono, archivos_img, archivos_vid, otros_archivos):
    """Muestra un resumen de los archivos encontrados."""
    total_archivos = len(archivos_img) + len(archivos_vid) + len(otros_archivos) + len(archivos_telefono)
    
    if total_archivos == 0:
        print("No se encontraron archivos para renombrar.")
        return False
    
    print(f"Se encontraron {total_archivos} archivos en total:\n")
    
    if archivos_telefono:
        print(f"[TELÉFONO] {len(archivos_telefono)} archivos con formato de teléfono:")
        for _, original in archivos_telefono:
            print(f"  {original}")
        print()
    
    if archivos_img:
        print(f"[IMG] {len(archivos_img)} archivos de imágenes:")
        for _, original in archivos_img:
            print(f"  {original}")
        print()
    
    if archivos_vid:
        print(f"[VID] {len(archivos_vid)} archivos de video:")
        for _, original in archivos_vid:
            print(f"  {original}")
        print()
    
    if otros_archivos:
        print(f"[OTROS] {len(otros_archivos)} otros archivos:")
        for _, original in otros_archivos:
            print(f"  {original}")
        print()
    
    return True

def mostrar_menu():
    """Muestra el menú principal y obtiene la opción seleccionada."""
    print("\nOpciones de conversión:")
    print("1. Todos los archivos")
    print("2. Archivos IMG")
    print("3. Archivos VID")
    print("4. Archivos IMG y VID")
    print("5. Archivos TELEFONO")
    print("6. Salir sin hacer cambios")
    
    while True:
        try:
            opcion = int(input("\nSeleccione una opción (1-6): "))
            if opcion in [1, 2, 3, 4, 5, 6]:
                return opcion
            print("\nPor favor, seleccione una opción válida (1-6)")
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