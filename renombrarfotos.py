import sys
import os

# Añadir el directorio 'src' al path para que Python encuentre el paquete 'renombrar'
# Esto es crucial tanto para ejecutar el script directamente como para PyInstaller
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from renombrar.main import main

if __name__ == "__main__":
    try:
        # Ajusta el sys.path para que las importaciones funcionen tanto en desarrollo como en el ejecutable
        if getattr(sys, 'frozen', False):
            # Estamos en un ejecutable de PyInstaller
            application_path = os.path.dirname(sys.executable)
            src_path = os.path.join(application_path, 'src')
        else:
            # Estamos en un entorno de desarrollo normal
            application_path = os.path.dirname(__file__)
            src_path = os.path.join(application_path, 'src')
        
        sys.path.insert(0, src_path)
        
        from renombrar.main import main
        main()
    except Exception as e:
        import traceback
        print("\n--- OCURRIÓ UN ERROR INESPERADO ---")
        print(f"Error: {e}")
        print("\n--- TRACEBACK ---")
        traceback.print_exc()
        print("\nLa aplicación se cerrará. Presione cualquier tecla para salir...")
        input()
