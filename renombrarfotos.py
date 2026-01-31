import sys
import os

if __name__ == "__main__":
    try:
        # Ajusta el sys.path para que las importaciones funcionen tanto en desarrollo como en el ejecutable
        if getattr(sys, 'frozen', False):
            # Estamos en un ejecutable de PyInstaller
            # PyInstaller bundlea todo en sys._MEIPASS internamente
            application_path = sys._MEIPASS
        else:
            # Estamos en un entorno de desarrollo normal
            application_path = os.path.dirname(__file__)
            src_path = os.path.join(application_path, 'src')
            sys.path.insert(0, src_path)
        
        from renombrar.main import main
        main()
    except ImportError as e:
        import traceback
        print("\n--- ERROR DE IMPORTACIÓN ---")
        print(f"No se pudo importar el módulo necesario: {e}")
        print("\n--- TRACEBACK ---")
        traceback.print_exc()
        print("\nVerifique que todos los archivos del programa estén presentes.")
        print("\nLa aplicación se cerrará. Presione cualquier tecla para salir...")
        input()
    except Exception as e:
        import traceback
        print("\n--- OCURRIÓ UN ERROR INESPERADO ---")
        print(f"Error: {e}")
        print("\n--- TRACEBACK ---")
        traceback.print_exc()
        print("\nLa aplicación se cerrará. Presione cualquier tecla para salir...")
        input()
