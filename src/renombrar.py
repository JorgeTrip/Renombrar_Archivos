import os
import re
import wave
import datetime

# Función para obtener la fecha y la hora a partir del nombre del archivo
def obtener_fecha_hora(nombre_archivo):
    # Expresión regular para buscar fechas y horas en el nombre del archivo
    patron = r'(\d{4})[-_.\s]?(\d{2})[-_.\s]?(\d{2})(?:.*?(\d{2})[-_.\s]?(\d{2})[-_.\s]?(\d{2}))?'

    coincidencia = re.search(patron, nombre_archivo)
    
    if coincidencia:
        # Construir la fecha con los grupos coincidentes
        fecha = f"{coincidencia.group(1)}-{coincidencia.group(2)}-{coincidencia.group(3)}"

        # Verificar si se encontró la hora en el nombre del archivo
        if coincidencia.group(4) and coincidencia.group(5) and coincidencia.group(6):
            # Construir la hora con los grupos coincidentes si se encontró
            hora = f"{coincidencia.group(4)}-{coincidencia.group(5)}-{coincidencia.group(6)}"
        else:
            hora = None  # Establecer la hora como None si no se encuentra en el nombre del archivo

        return fecha, hora
    else:
        return None, None  # Si no se encuentra la fecha, retornar None para ambas variables

def obtener_nombre_destino(nombre_archivo, secuencia):
    fecha, hora = obtener_fecha_hora(nombre_archivo)

    if fecha:
        nombre_base, extension = os.path.splitext(nombre_archivo)
        if hora:
            return f"{fecha} {hora}{extension}"
        else:
            secuencia = secuencia + 1
            return f"{fecha} {nombre_base.split('-')[-1]}{extension}"
    else:
        return nombre_archivo

def obtener_nombre_destino_letra(nombre_archivo, letra):
    fecha, hora = obtener_fecha_hora(nombre_archivo)
    
    if fecha:
        if hora:
            nombre_base, extension = os.path.splitext(nombre_archivo)
            return f"{fecha} {hora}{letra}{extension}"
        else:
            return None  # No debería cambiar el nombre si no hay hora
    else:
        return None  # No debería cambiar el nombre si no hay fecha

def archivo_tiene_formato_destino(nombre_archivo):
    # Expresión regular para verificar si el archivo ya tiene el formato de nombre de destino
    patron_destino = r'(\d{4}-\d{2}-\d{2}\s\d{2}-\d{2}-\d{2})\.\w+'
    return re.match(patron_destino, nombre_archivo) is not None

def main():
    print("Renombrar archivos de fotos y videos")
    print("---> by JOT <---")
    print("==========================================")
    print("\nIniciando búsqueda de archivos a renombrar...")
    
    secuencia = 0
    archivos_renombrados = 0
    cambios_realizados = []
    
    # Lista de extensiones de archivo permitidas
    extensiones_permitidas = (".jpg", ".jpeg", ".png", ".mkv", ".mp4")
    
    for directorio_raiz, _, archivos in os.walk(os.getcwd()):
        for nombre_archivo in archivos:
            # Filtrar archivos por extensión permitida y que no tengan el formato de nombre de destino
            if nombre_archivo.lower().endswith(extensiones_permitidas) and not archivo_tiene_formato_destino(nombre_archivo):
                nuevo_nombre = obtener_nombre_destino(nombre_archivo, secuencia)
                ruta_completa_original = os.path.join(directorio_raiz, nombre_archivo)
                ruta_completa_destino = os.path.join(directorio_raiz, nuevo_nombre)

                # Verificar si el archivo ya existe en el directorio de destino
                if ruta_completa_original != ruta_completa_destino:
                    # Si el archivo ya existe, preguntar al usuario qué desea hacer
                    if os.path.exists(ruta_completa_destino):
                        print()
                        print(f"Error al intentar renombrar archivo \"{nombre_archivo}\":")
                        print(f"El archivo \"{nuevo_nombre}\" ya existe.")

                        while True:
                            opcion_letra = ""  # Inicializar opcion_letra
                            print()
                            print("Opciones:")
                            print("a. Renombrar agregando letra al final")
                            print("b. No hacer nada (omitir renombrar)")
                            opcion = input("\n¿Qué desea hacer? (a/b): ")

                            if opcion.lower() == 'a':
                                secuencia_letra = 'a'
                                while os.path.exists(ruta_completa_destino):
                                    nuevo_nombre = obtener_nombre_destino_letra(nombre_archivo, secuencia_letra)
                                    if nuevo_nombre is not None:
                                        ruta_completa_destino = os.path.join(directorio_raiz, nuevo_nombre)
                                        if not os.path.exists(ruta_completa_destino):
                                            os.rename(ruta_completa_original, ruta_completa_destino)  # Renombrar el archivo
                                            archivos_renombrados += 1
                                            cambios_realizados.append((nombre_archivo, nuevo_nombre))
                                            break  # El nuevo nombre es único, salir del bucle
                                    else:
                                        print(f"El archivo \"{nuevo_nombre}\" también existe.")
                                        print("Opciones:")
                                        print("a. Probar agregar la siguiente letra disponible")
                                        print("b. No renombrar")
                                        opcion_letra = input("\n¿Qué desea hacer? (a/b): ")
                                        if opcion_letra.lower() == 'b':
                                            break  # No renombrar
                                        secuencia_letra = chr(ord(secuencia_letra) + 1)  # Obtener la siguiente letra
                                if opcion_letra.lower() == 'a':
                                    os.rename(ruta_completa_original, ruta_completa_destino)
                                    archivos_renombrados += 1
                                    cambios_realizados.append((nombre_archivo, nuevo_nombre))
                                break 
                            elif opcion.lower() == 'b':
                                break
                            else:
                                print()
                                print("Opción no válida. Por favor, seleccione 'a' o 'b'.")
                    elif nombre_archivo != nuevo_nombre:  # Verificar si los nombres son diferentes, antes de renombrar
                        os.rename(ruta_completa_original, ruta_completa_destino)
                        archivos_renombrados += 1
                        cambios_realizados.append((nombre_archivo, nuevo_nombre))
    
    if archivos_renombrados == 0:
        print("\nNo hay archivos por renombrar.")
    else:
        print("\nProceso de cambio de nombre finalizado con éxito.")
        print()
        print(f"Se realizaron {archivos_renombrados} cambios:")
        for cambio in cambios_realizados:
            print(f"{cambio[0]} --> {cambio[1]}")
    
    print("==========================================")
    print()
    input("Presione cualquier tecla para salir...")

if __name__ == "__main__":
    main()

