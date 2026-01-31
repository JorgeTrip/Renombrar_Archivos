import os
import sys

# Añadir el directorio 'src' al sys.path para que los módulos se encuentren
# tanto en desarrollo como en el ejecutable de PyInstaller.
if getattr(sys, 'frozen', False):
    # Estamos en un ejecutable de PyInstaller
    application_path = os.path.dirname(sys.executable)
    sys.path.insert(0, os.path.abspath(os.path.join(application_path, '..')))
else:
    # Estamos en un entorno de desarrollo
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from renombrar.core.file_utils import (
    obtener_nombre_destino,
    obtener_nombre_destino_letra,
    renombrar_archivo,
    encontrar_archivos_por_directorio
)
from renombrar.core.date_utils import tiene_formato_telefono
from renombrar.ui.menu import (
    seleccionar_directorios,
    mostrar_resumen_archivos,
    mostrar_menu,
    mostrar_opciones_duplicado,
    preguntar_continuar,
    mostrar_titulo,
    mostrar_bienvenida,
    mostrar_copyright_salida
)

def main():
    """Función principal del programa."""
    directorio_base = os.getcwd()
    extensiones_permitidas = (".jpg", ".jpeg", ".png", ".mkv", ".mp4", ".heic")
    
    # Mostrar pantalla de bienvenida solo la primera vez
    if not mostrar_bienvenida():
        print("\nPrograma cancelado por el usuario.")
        mostrar_copyright_salida()
        input("\nPresione cualquier tecla para salir...")
        return

    while True:
        mostrar_titulo()
        print(f"Buscando archivos en '{directorio_base}' y subdirectorios...\n")

        archivos_por_directorio = encontrar_archivos_por_directorio(directorio_base)
        
        if not archivos_por_directorio:
            print("=" * 70)
            print("NO SE ENCONTRARON ARCHIVOS PARA RENOMBRAR")
            print("=" * 70)
            print()
            print("El programa no encontró archivos con patrones de nombre reconocibles")
            print("en el directorio actual.")
            print()
            print("RECORDATORIO:")
            print("  • Este programa debe ejecutarse en la carpeta que contiene")
            print("    las fotos o videos a renombrar.")
            print("  • El programa busca archivos con patrones como:")
            print("    - IMG_YYYYMMDD_HHMMSS.jpg")
            print("    - VID_YYYYMMDD_HHMMSS.mp4")
            print("    - YYYYMMDD_HHMMSS.* (formato teléfono)")
            print()
            print(f"Directorio actual: {directorio_base}")
            print()
            
            while True:
                respuesta = input("¿Desea salir del programa? (s/n): ").lower().strip()
                if respuesta in ['s', 'n']:
                    if respuesta == 's':
                        mostrar_copyright_salida()
                        input("\nPresione cualquier tecla para salir...")
                        return
                    else:
                        break
                print("Por favor, responda con 's' para sí o 'n' para no.")
            
            # Si el usuario dice 'n', continuar el ciclo para volver a buscar
            continue

        directorios_seleccionados = seleccionar_directorios(archivos_por_directorio)
        if not directorios_seleccionados:
            print("\nNo se seleccionaron directorios. Saliendo.")
            mostrar_copyright_salida()
            input("\nPresione cualquier tecla para salir...")
            return

        # Clasificar archivos de los directorios seleccionados
        archivos_clasificados = {
            'archivos_img': [], 'archivos_vid': [], 'otros_archivos': [],
            'archivos_telefono': [], 'archivos_sugeridos': []
        }
        
        # Clasificar archivos, generando nombres de destino sobre la marcha
        secuencia = 0
        for dir_rel in directorios_seleccionados:
            for nombre_archivo in archivos_por_directorio[dir_rel]:
                nuevo_nombre = obtener_nombre_destino(nombre_archivo, secuencia)
                if nombre_archivo == nuevo_nombre:
                    continue  # Ignorar archivos que no coinciden con ningún patrón

                # Si el nombre cambia, es un candidato. La secuencia solo aumenta para ellos.
                secuencia += 1
                
                archivo_info = (dir_rel, nombre_archivo, nuevo_nombre)
                nombre_upper = nombre_archivo.upper()
                extension_coincide = nombre_archivo.lower().endswith(extensiones_permitidas)

                if not extension_coincide:
                    archivos_clasificados['archivos_sugeridos'].append(archivo_info)
                    continue

                if tiene_formato_telefono(nombre_archivo):
                    archivos_clasificados['archivos_telefono'].append(archivo_info)
                elif nombre_upper.startswith("IMG"):
                    archivos_clasificados['archivos_img'].append(archivo_info)
                elif nombre_upper.startswith("VID"):
                    archivos_clasificados['archivos_vid'].append(archivo_info)
                else:
                    archivos_clasificados['otros_archivos'].append(archivo_info)

        if not mostrar_resumen_archivos(archivos_clasificados):
            mostrar_copyright_salida()
            input("\nPresione cualquier tecla para salir...")
            return

        categorias_a_procesar = mostrar_menu(archivos_clasificados)
        if not categorias_a_procesar:
            print("\nOperación cancelada.")
            mostrar_copyright_salida()
            input("\nPresione cualquier tecla para salir...")
            return
        
        archivos_a_procesar = []
        for categoria in categorias_a_procesar:
            archivos_a_procesar.extend(archivos_clasificados.get(categoria, []))

        if not archivos_a_procesar:
            print("\nNo hay archivos en las categorías seleccionadas.")
            if not preguntar_continuar():
                return
            else:
                continue

        # Proceder con el renombrado
        print(f"\nProcediendo con el renombrado de {len(archivos_a_procesar)} archivos...")
        archivos_renombrados = 0
        cambios_realizados = []

        secuencia = 0
        for dir_rel, nombre_archivo, nuevo_nombre_original in archivos_a_procesar:
            # El nuevo nombre ya fue calculado, pero lo recalculamos por si la secuencia cambió
            nuevo_nombre = obtener_nombre_destino(nombre_archivo, secuencia)
            if nombre_archivo == nuevo_nombre:
                continue
            
            # Incrementar la secuencia para el siguiente archivo válido
            secuencia += 1
            
            # Reconstruir la ruta absoluta para las operaciones de renombrado
            directorio_absoluto = os.path.abspath(os.path.join(directorio_base, dir_rel))
            ruta_completa_original = os.path.join(directorio_absoluto, nombre_archivo)
            ruta_completa_destino = os.path.join(directorio_absoluto, nuevo_nombre)

            if os.path.exists(ruta_completa_destino):
                opcion = mostrar_opciones_duplicado(nombre_archivo, nuevo_nombre)
                
                if opcion == 'a':
                    secuencia_letra = 'a'
                    while os.path.exists(ruta_completa_destino):
                        nuevo_nombre = obtener_nombre_destino_letra(nombre_archivo, secuencia_letra)
                        if nuevo_nombre is not None:
                            ruta_completa_destino = os.path.join(directorio_absoluto, nuevo_nombre)
                            if not os.path.exists(ruta_completa_destino):
                                if renombrar_archivo(ruta_completa_original, ruta_completa_destino):
                                    archivos_renombrados += 1
                                    cambios_realizados.append((nombre_archivo, nuevo_nombre))
                                break
                        secuencia_letra = chr(ord(secuencia_letra) + 1)
            else:
                if renombrar_archivo(ruta_completa_original, ruta_completa_destino):
                    archivos_renombrados += 1
                    cambios_realizados.append((nombre_archivo, nuevo_nombre))

        print("\nProceso de cambio de nombre finalizado.")
        print(f"\nSe realizaron {archivos_renombrados} cambios:")
        for cambio in cambios_realizados:
            print(f"{cambio[0]} --> {cambio[1]}")
        
        print("==========================================")
        
        if not preguntar_continuar():
            print("\nPresione cualquier tecla para salir...")
            input()
            return
            
        print("\n" + "="*50 + "\n")  # Separador visual entre iteraciones

# El bloque if __name__ == '__main__' se moverá a un script de entrada (run.py)
# para evitar problemas con la ejecución de paquetes y PyInstaller.
# Si se necesita ejecutar este archivo directamente para pruebas, se puede descomentar.
# if __name__ == "__main__":
#     main() 