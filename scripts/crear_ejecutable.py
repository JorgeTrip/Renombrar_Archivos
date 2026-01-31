import os
import subprocess
import sys

def crear_ejecutable():
    """Crea un ejecutable .exe del programa usando PyInstaller."""
    try:
        # Instalar PyInstaller si no está instalado
        print("Verificando PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"], 
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Obtener rutas del proyecto
        project_root = os.path.dirname(os.path.dirname(__file__))
        scripts_dir = os.path.join(project_root, 'scripts')
        spec_file = os.path.join(scripts_dir, 'RenombrarFotos.spec')
        dist_dir = os.path.join(project_root, 'dist')
        
        # Verificar que el spec file existe
        if not os.path.exists(spec_file):
            print(f"ERROR: No se encuentra el archivo {spec_file}")
            print("El archivo de configuración .spec es necesario para la compilación.")
            input("\nPresione Enter para salir...")
            return
        
        print(f"\nUsando configuración: {spec_file}")
        print("Compilando...")
        print("=" * 60)
        
        # Compilar usando el spec file pre-configurado
        # --clean asegura una compilación limpia
        subprocess.check_call([
            sys.executable, 
            "-m", 
            "PyInstaller",
            spec_file,
            "--clean"
        ])
        
        exe_path = os.path.join(dist_dir, 'RenombrarFotos.exe')
        
        print("\n" + "=" * 60)
        print("✓ Ejecutable creado exitosamente!")
        print(f"✓ Ubicación: {exe_path}")
        print("=" * 60)
        
        if os.path.exists(exe_path):
            size_mb = os.path.getsize(exe_path) / (1024 * 1024)
            print(f"✓ Tamaño: {size_mb:.2f} MB")
        
    except subprocess.CalledProcessError as e:
        print(f"\n✗ Error durante la compilación.")
        print(f"Código de salida: {e.returncode}")
    except Exception as e:
        print(f"\n✗ Error al crear el ejecutable: {e}")
        import traceback
        traceback.print_exc()
    
    input("\nPresione Enter para salir...")

if __name__ == "__main__":
    crear_ejecutable()
 