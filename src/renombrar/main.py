import os
from .core.file_utils import (
    obtener_nombre_destino,
    obtener_nombre_destino_letra,
    renombrar_archivo,
    buscar_archivos
)
from .core.date_utils import archivo_tiene_formato_destino
from .ui.menu import (
    mostrar_resumen_archivos,
    mostrar_menu,
    mostrar_opciones_duplicado,
    preguntar_continuar
)

def main():
    """Función principal del programa."""
    while True:
        print("Renombrar archivos de fotos y videos")
        print("---> by JOT <---")
        print("==========================================")
        print("\nBuscando archivos para renombrar en el directorio actual...\n")
        
        secuencia = 0
        extensiones_permitidas = (".jpg", ".jpeg", ".png", ".mkv", ".mp4", ".heic")
        
        # Buscar archivos
        archivos_img, archivos_vid, otros_archivos, archivos_telefono = buscar_archivos(
            os.getcwd(), extensiones_permitidas
        )
        
        # Mostrar resumen y obtener opción
        if not mostrar_resumen_archivos(archivos_telefono, archivos_img, archivos_vid, otros_archivos):
            print("==========================================")
            input("\nPresione cualquier tecla para salir...")
            return
            
        opcion = mostrar_menu()
        
        # Determinar qué archivos procesar
        archivos_a_procesar = []
        if opcion == 1:
            archivos_a_procesar = archivos_telefono + archivos_img + archivos_vid + otros_archivos
        elif opcion == 2:
            archivos_a_procesar = archivos_img
        elif opcion == 3:
            archivos_a_procesar = archivos_vid
        elif opcion == 4:
            archivos_a_procesar = archivos_img + archivos_vid
        elif opcion == 5:
            archivos_a_procesar = archivos_telefono
        else:  # opcion == 6
            print("\nOperación cancelada.")
            print("==========================================")
            input("\nPresione cualquier tecla para salir...")
            return

        # Proceder con el renombrado
        print(f"\nProcediendo con el renombrado de {len(archivos_a_procesar)} archivos...")
        archivos_renombrados = 0
        cambios_realizados = []

        for directorio_raiz, nombre_archivo in archivos_a_procesar:
            nuevo_nombre = obtener_nombre_destino(nombre_archivo, secuencia)
            if nombre_archivo == nuevo_nombre:
                continue
                
            ruta_completa_original = os.path.join(directorio_raiz, nombre_archivo)
            ruta_completa_destino = os.path.join(directorio_raiz, nuevo_nombre)

            if os.path.exists(ruta_completa_destino):
                opcion = mostrar_opciones_duplicado(nombre_archivo, nuevo_nombre)
                
                if opcion == 'a':
                    secuencia_letra = 'a'
                    while os.path.exists(ruta_completa_destino):
                        nuevo_nombre = obtener_nombre_destino_letra(nombre_archivo, secuencia_letra)
                        if nuevo_nombre is not None:
                            ruta_completa_destino = os.path.join(directorio_raiz, nuevo_nombre)
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

if __name__ == "__main__":
    main() 